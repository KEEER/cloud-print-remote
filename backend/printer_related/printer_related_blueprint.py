from utils.user_status_detection import login_required
from backend.account_related.session_manager import get_session_by_token
from utils.security import secured_sign
from backend.independent.price_calculation import calculate_price
# [Python native modules]
import logging
# [Third-party modules]
from flask import Blueprint, request

logger = logging.getLogger(__name__)
class CONSTS:
    class ROUTES:
        PRINT = '/_api/print'
printer_related_blueprint = Blueprint('printer_related_blueprint', __name__)

@printer_related_blueprint.route(CONSTS.ROUTES, methods = ['GET'])
def process_print():
    configs