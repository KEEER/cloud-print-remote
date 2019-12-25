# [In-project modules]
from utils.user_status_detection import login_required
from backend.account_related.session_manager import get_session_by_token, get_session_by_code
from utils.kas_manager import pay, login, token_is_valid, get_kredit_amount
from utils.security import secured_sign, verify
from config import ServerConfig
# [Python native modules]
import logging
import json
import random
import time
# [Third-party modules]
from flask import Blueprint, request, render_template, redirect, make_response

class CONSTS:
    TOKEN = 'kas-account-token'
    JOB_NUMBER_LIMIT = 1000
    INVALID_FORM = ('Invalid Form', 400)
    ILLEGAL_REQUEST = ('Illegal Request', 401)
    class ROUTES:
        REQUEST_JOB_TOKEN = '/_api/job-token'
        REQUEST_SESSION = '/_api/session'
        DELETE_JOB_TOKEN = '/_api/delete-job'
        LOGIN = '/login'
        INDEX = '/'
        

account_related_blueprint = Blueprint('account_related_blueprint', __name__)
logger = logging.getLogger(__name__)

@account_related_blueprint.route(CONSTS.ROUTES.LOGIN, methods = ['GET'])
def index():
    return redirect(login())
    
@account_related_blueprint.route(CONSTS.ROUTES.INDEX, methods = ['GET', 'POST'])
def process_index():
    return render_template('index.html')

@account_related_blueprint.route(CONSTS.ROUTES.REQUEST_JOB_TOKEN, methods = ['GET'])
@login_required
def process_request_job_token():
    # access the token
    token = request.cookies.get(CONSTS.TOKEN, '')
    code = request.args.get('code', '')

    session = get_session_by_token(token)
    debt = session.get_debt()
    if debt > 0:
        # there's debt
        # try to pay the debt
        pay_result = pay(session.get_kiuid(), debt)
        if pay_result[0]:
            # successful
            session.remove_all_debt()
        else:
            # TODO: maybe add a record
            return 'You have debt to pay; access denied.', 401
        # maybe we need to make a debt page.
    
    timestamp = str(int(time.time()))
    if code == '':
        # new task mode
        if session.job_number < CONSTS.JOB_NUMBER_LIMIT:
            code = session.add_job()
            
            return json.dumps({
                'code': code,
                'timestamp': timestamp,
                'sign': secured_sign(code+timestamp)
            })
        # in legal cases this will NEVER happen so... the format doesn't matter here
        # this shall be prevented from the front end.
        return json.dumps({
            'status': 1,
            'message': 'Too many jobs.'
        })
    else:
        if not session.has_job(code):
            # a fake code
            return CONSTS.INVALID_FORM
        else:
            return json.dumps({
                'code': code,
                'timestamp': timestamp,
                'sign': secured_sign(code + timestamp)
            })

    
@account_related_blueprint.route(CONSTS.ROUTES.REQUEST_SESSION, methods = ['GET'])
@login_required
def process_request_session():
    token = request.cookies.get(CONSTS.TOKEN,'')
    
    session = get_session_by_token(token)
    jobs = session.get_all_jobs()
    kredit = get_kredit_amount(token)
    timestamp = str(int(time.time()))
    logger.debug('[in request session] Session=> '+str(session))
    return json.dumps({
        'codes': jobs,
        'kredit': kredit,
        'timestamp': timestamp,
        'debt': session.get_debt(),
        'sign': secured_sign(','.join(jobs)+timestamp)
    })

@account_related_blueprint.route('/__api/delete', methods = ['GET'])
@login_required
def process_delete_all_codes():
    token = request.cookies.get(CONSTS.TOKEN, '')
    session = get_session_by_token(token)
    session._jobs = []
    session.save()
    return 'All clear.'
    
@account_related_blueprint.route(CONSTS.ROUTES.DELETE_JOB_TOKEN, methods = ['GET'])
def process_delete_job_token():
    code = request.args.get('code', '')
    sign = request.args.get('sign', '')
    if code == '':
        return CONSTS.INVALID_FORM
    if sign == '' or not verify(code, sign):
        if request.cookies.get('kas-account-token', '') == '':
            return redirect(login())
        elif not token_is_valid(request.cookies.get('kas-account-token')):
            response = make_response(redirect(login()))
            if not ServerConfig.debug:
                # in the real server
                response.set_cookie('kas-account-token', '', max_age = 0, domain = '.keeer.net')
            else:
                response.set_cookie('kas-account-token', '', max_age = 0)
            return response
    
    session = get_session_by_code(code)
    logger.debug('[in delete job] Session=> '+str(session))
    if session != None:
        session.remove_job(code)
        del(session)
    else:
        return json.dumps({
            'status': 1,
            'message': 'code does not exist'
        })
    return json.dumps({
            'status': 0,
            'message': 'code removed'
        })