# [In-project modules]
from backend.independent.price_calculation import calculate_price
# [Python native modules]
import logging
import json
# [Third-party modules]
from flask import Blueprint, request

class CONSTS:
    class ROUTES:
        CALCULATE_PRICE = '/_api/calculate-price'
    INVALID_FORM = ('Invalid form', 400)

independent_blueprint = Blueprint('independent_blueprint', __name__)
logger = logging.getLogger(__name__)


@independent_blueprint.route(CONSTS.ROUTES.CALCULATE_PRICE)
def process_calculate_price():
	config = request.args.get('config', '')
	printer = request.args.get('printer_id', '')
	if config == '' or printer == '':
		return CONSTS.INVALID_FORM
	config = json.loads(config)
	logger.debug('Config: '+ str(config))
	price = calculate_price(config, printer)
	if price < 0:
		return json.dumps({
			'status': 1,
			'result': '不合理的打印配置'
		})
	else:
		return json.dumps({
			'status': 0,
			'result': price
		})

	