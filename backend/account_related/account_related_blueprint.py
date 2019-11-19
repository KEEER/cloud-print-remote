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
            code = random.randint(1000, 9999)
            nonce = str(uuid.uuid1())
            session.add_job(code)
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

    
