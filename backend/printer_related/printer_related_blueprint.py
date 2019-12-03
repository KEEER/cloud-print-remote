from utils.user_status_detection import login_required
from backend.account_related.session_manager import get_session_by_code
from utils.security import secured_sign, verify
from backend.independent.price_calculation import calculate_price
from utils.kas_manager import pay
# [Python native modules]
import logging
# [Third-party modules]
from flask import Blueprint, request

logger = logging.getLogger(__name__)
class CONSTS:
    class ROUTES:
        PRINT = '/_api/print'
    INVALID_FORM = ('Invalid form', 400)
printer_related_blueprint = Blueprint('printer_related_blueprint', __name__)

@printer_related_blueprint.route(CONSTS.ROUTES, methods = ['GET'])
def process_print():
    code = request.args.get('code', '')
    printer_id = request.args.get('id', '')
    config = request.args.get('configs', '')
    sign = request.args.get('sign', '')
    if config == '' or sign == '' or code == '' or printer_id == '':
        return CONSTS.INVALID_FORM
    if not verify(code + config, sign):
        return 'Wrong Signature', 401
    session = get_session_by_code(code)

    pay_result = pay(session.get_kiuid(), session.get_debt())
    if pay_result[0]:
        # successful
        session.remove_all_debt()
    else:
        # TODO: maybe add a record
        return 'You have debt to pay; access denied.', 401

    price = calculate_price(config, printer_id)
    if price < 0:
        return CONSTS.INVALID_FORM
    kiuid = session.get_kiuid()
    payment_result = pay(kiuid, price)
    
    if not payment_result[0]:
        logger.info('Payment failed: %s'%payment_result[1])
        session.add_debt(price)

    session.remove_job(code)