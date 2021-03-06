# [In-project modules]
from utils.user_status_detection import login_required
from backend.account_related.session_manager import get_session_by_token, get_session_by_code
from utils.kas_manager import pay, login, token_is_valid, get_kredit_amount
from utils.security import secured_sign, verify
from config import ServerConfig
from utils.json_logger import JSONLogger
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
        DELETE_JOB_TOKEN = '/_api/delete-job-token'
        LOGIN = '/login'
        INDEX = '/'
        QUICK_CODES = '/quick-codes'
        

account_related_blueprint = Blueprint('account_related_blueprint', __name__)
logger = logging.getLogger(__name__)

account_logger = JSONLogger('logs/account.log')

job_logger = JSONLogger('logs/job.log')

@account_related_blueprint.route(CONSTS.ROUTES.LOGIN, methods = ['GET'])
def index():
    return redirect(login())
    
@account_related_blueprint.route(CONSTS.ROUTES.INDEX, methods = ['GET', 'POST'])
@login_required
def process_index():
    return render_template('index.html')

@account_related_blueprint.route(CONSTS.ROUTES.REQUEST_JOB_TOKEN, methods = ['GET'])
def process_request_job_token():
    # access the token
    code = request.args.get('code', '')
    token = request.cookies.get(CONSTS.TOKEN, '')
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
    if session.get_debt() > 0:
        payment_result = pay(session.get_kiuid(), session.get_debt())
        
        if not payment_result[0]:
            logger.info('Still in debt.')
        else:
            session.remove_all_debt()

    logger.debug('[in request session] Session=> '+str(session))

    account_logger.write(json.dumps({
        'time': time.time(),
        'kredit': kredit,
        'debt': session.get_debt(),
        'kiuid': session.get_kiuid()
    }))

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
        job_logger.write(json.dumps({
            'time': time.time(),
            'code': code,
            'kiuid': session.get_kiuid()
        }))
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

@account_related_blueprint.route(CONSTS.ROUTES.QUICK_CODES, methods = ['GET'])
def process_quick_codes():
    codes = request.args.get('codes', '')
    if codes == '':
        return CONSTS.INVALID_FORM
    codes = json.loads(codes)
    return render_template('quick-codes.html', CODES = codes)
