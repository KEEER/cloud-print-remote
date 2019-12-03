# [In-project modules]
from utils.user_status_detection import login_required
from backend.account_related.session_manager import get_session_by_token, get_session_by_code
from utils.kas_manager import pay
from utils.security import secured_sign, verify
# [Python native modules]
import logging
import json
import random
import time
# [Third-party modules]
from flask import Blueprint, request

class CONSTS:
    TOKEN = 'kas-account-token'
    JOB_NUMBER_LIMIT = 3
    INVALID_FORM = ('Invalid Form', 400)
    ILLEGAL_REQUEST = ('Illegal Request', 401)
    class ROUTES:
        REQUEST_JOB_TOKEN = '/_api/job-token'
        REQUEST_JOB_CODES = '/_api/codes'
        DELETE_JOB_TOKEN = '/_api/delete-job-token'
        

account_related_blueprint = Blueprint('account_related_blueprint', __name__)
logger = logging.getLogger(__name__)


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
    if code == '':
        # new task mode
        if session.job_number < CONSTS.JOB_NUMBER_LIMIT:
            code = session.add_job(code)
            timestamp = int(time.time())
            
            return json.dumps({
                'code': code,
                'timestamp': timestamp,
                'sign': secured_sign(code+timestamp)
            })
        # in legal cases this will NEVER happen so... the format doesn't matter here
        # this shall be prevented from the front end.
        return 'Too many jobs.'
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

    
@account_related_blueprint.route(CONSTS.ROUTES.REQUEST_JOB_CODES, methods = ['GET'])
@login_required
def process_request_job_codes():
    token = request.cookies.get(CONSTS.TOKEN,'')
    session = get_session_by_token(token)
    jobs = session.get_all_jobs()
    return json.dumps({
        'codes': jobs,
        'sign': secured_sign(','.join(jobs))
    })

@account_related_blueprint.route(CONSTS.ROUTES.DELETE_JOB_TOKEN, methods = ['GET'])
def process_delete_job_token():
    code = request.args.get('code', '')
    sign = request.args.get('sign', '')
    if code == '' or sign == '':
        return CONSTS.INVALID_FORM
    if not verify(code, sign):
        return CONSTS.ILLEGAL_REQUEST
    
    session = get_session_by_code(code)
    if session != None:
        session.remove_job(code)
    else:
        return json.dumps({
            'status': 1,
            'message': 'code does not exist'
        })
    return json.dumps({
            'status': 0,
            'message': 'code removed'
        })