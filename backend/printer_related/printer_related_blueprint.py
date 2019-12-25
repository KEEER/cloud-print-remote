from utils.user_status_detection import login_required
from backend.account_related.session_manager import get_session_by_code
from utils.security import secured_sign, verify
from backend.independent.price_calculation import calculate_price
from utils.kas_manager import pay
# [Python native modules]
import logging
import json
import pickle
from string import Template
import time
# [Third-party modules]
from flask import Blueprint, request

logger = logging.getLogger(__name__)
class CONSTS:
    class ROUTES:
        REQUEST_GET_IPS_TOKEN='/_api/printer-ips'
        REQUEST_SET_IPS_TOKEN='/_api/printer-ip'
        PRINT = '/_api/print'
        REQUEST_GET_JOB_TOKEN='/_api/printer-ips'
        REQUEST_SET_JOB_TOKEN='/_api/printer-ip'
        STATUS_REPORT='/_api/status-report'
    INVALID_FORM = ('Invalid form', 400)

printer_related_blueprint = Blueprint('printer_related_blueprint', __name__)

@printer_related_blueprint.route(CONSTS.ROUTES.PRINT, methods = ['POST'])
def process_print():
    code = request.form.get('code', '')
    printer_id = request.form.get('id', '')
    config = request.form.get('config', '')
    sign = request.form.get('sign', '')

    for k,v in request.form.items():
        logger.debug('%s -> %s'%(k,v))
    logger.debug(code+ printer_id+config+sign)

    if config == '' or sign == '' or code == '' or printer_id == '':
        return CONSTS.INVALID_FORM
    if not verify(code + config + printer_id, sign):
        return 'Wrong Signature', 401
    config = json.loads(config)
    session = get_session_by_code(code)
    if session.get_debt() > 0:
        pay_result = pay(session.get_kiuid(), session.get_debt())
        if pay_result[0]:
            # successful
            session.remove_all_debt()
        else:
            # TODO: maybe add a record
            return json.dumps({
                'status': 1,
                'message': 'Payment Failed: this user has debt'
            })

    price = calculate_price(config, printer_id)
    if price < 0:
        logger.debug('Price:'+str(price))
        return CONSTS.INVALID_FORM
    kiuid = session.get_kiuid()
    logger.debug('Price: '+ str(price))
    payment_result = pay(kiuid, price)
    
    if not payment_result[0]:
        logger.info('Payment failed: %s'%payment_result[1])
        session.add_debt(price)
        return json.dumps({
            'status': 2,
            'message': '支付失败'
        })
    session.remove_job(code)
    return json.dumps({
        'status': 0,
        'message': 'ok.'
    })

@printer_related_blueprint.route(CONSTS.ROUTES.REQUEST_GET_IPS_TOKEN,methods=['GET'])
def RequestPrinterIPs():
    current_db={}
    try:
        with open('./runtime_ipdb.pkl','rb') as pkl_file:
            current_db=pickle.load(pkl_file)
            pkl_file.close()
    except Exception as e:
        logger.debug(e)
    return json.dumps(current_db)

@printer_related_blueprint.route(CONSTS.ROUTES.REQUEST_SET_IPS_TOKEN,methods=['POST'])
def UpdatePrinterIP():
    ida=request.form.get('id','')
    ipa=request.form.get('ip','')
    sign=request.form.get('sign','')
    
    for k,v in request.form.items():
        logger.debug('%s -> %s'%(k,v))

    if not (verify(ida+ipa,sign)):
    	return 'Wrong Signature'

    current_db={}
    try:
        with open('./runtime_ipdb.pkl','rb') as pkl_file:
            current_db=pickle.load(pkl_file)
            pkl_file.close()
    except Exception as e:
        logger.debug(e)
    if ida in current_db:
        current_db[ida]=ipa
    else:
        current_db.update({ ida: ipa })
    with open('./runtime_ipdb.pkl','wb') as pkl_file:
        pickle.dump(current_db,pkl_file)
        pkl_file.flush()
        pkl_file.close()
        
    return json.dumps({
        'status': 0,
        'message': 'ok.'
    })

@printer_related_blueprint.route(CONSTS.ROUTES.STATUS_REPORT,methods=['POST'])
@login_required
def StatusReport():
    response = request.args.get('response', '')
    response = json.loads(response)
    
    toReadableMessage = Template('报告时间：${time} 打印机${name} 位于{geolocation}出现问题：\n{message}')

    nowtime = time.strftime('%Y.%m.%d',time.localtime(time.time()))
    readableMessage = toReadableMessage.safe_substitute(time = nowtime, name = response['name'], geolocation = response['geolocation'], message = response['message'])
    # TODO: Call maintainer
