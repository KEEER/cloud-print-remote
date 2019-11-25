# [In-project modules]
from utils.user_status_detection import login_required
from backend.account_related.session_manager import get_session_by_token
from utils.security import secured_sign
# [Python native modules]
import logging
import json
import random
import uuid
# [Third-party modules]
from flask import Blueprint, request

class CONSTS:
    TOKEN = 'kas-account-token'
    JOB_NUMBER_LIMIT = 3
    INVALID_FORM = ('Invalid Form', 400)
    class ROUTES:
        REQUEST_JOB_TOKEN = '/_api/job-token'
        REQUEST_JOB_CODES = '/_api/codes'
        

account_related_blueprint = Blueprint('account_related_blueprint', __name__)
logger = logging.getLogger(__name__)

@account_related_blueprint.route(CONSTS.ROUTES.REQUEST_JOB_TOKEN, methods = ['GET'])
@login_required
def process_request_job_token():
    # access the token
    token = request.cookies.get(CONSTS.TOKEN, '')
    code = request.args.get('code', '')

    session = get_session_by_token(token)
    if code == '':
        # new task mode
        if session.job_number < CONSTS.JOB_NUMBER_LIMIT:
            code = session.add_job(code)
            nonce = str(uuid.uuid1())
            
            return json.dumps({
                'code': code,
                'nonce': nonce,
                'sign': secured_sign(code+nonce)
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
                'nonce': nonce,
                'sign': secured_sign(code+nonce)
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