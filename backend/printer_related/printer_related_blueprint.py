from utils.user_status_detection import login_required
from backend.account_related.session_manager import get_session_by_code
from utils.security import secured_sign, verify
from backend.independent.price_calculation import calculate_price
from utils.kas_manager import pay
# [Python native modules]
import logging
import json
from string import Template
import time
# [Third-party modules]
from flask import Blueprint, request

logger = logging.getLogger(__name__)
class CONSTS:
    class ROUTES:
        PRINT = '/_api/print'
        REQUEST_GET_JOB_TOKEN='/_api/printer-ips'
        REQUEST_SET_JOB_TOKEN='/_api/printer-ip'
        STATUS_REPORT='/_api/status-report'
    INVALID_FORM = ('Invalid form', 400)
printer_related_blueprint = Blueprint('printer_related_blueprint', __name__)

@printer_related_blueprint.route(CONSTS.ROUTES.PRINT, methods = ['GET'])
def process_print():
    code = request.args.get('code', '')
    printer_id = request.args.get('id', '')
    config = request.args.get('configs', '')
    sign = request.args.get('sign', '')
    if config == '' or sign == '' or code == '' or printer_id == '':
        return CONSTS.INVALID_FORM
    if not verify(code + config, sign):
        return 'Wrong Signature', 401
    config = json.loads(config)
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

"""
@printer_related_blueprint.route(CONSTS.ROUTES.REQUEST_GET_JOB_TOKEN,methods=['GET'])
@login_required
def RequestPrinterIPs():
    try:
        result=[]
        with open('./runtime_ipdb') as rdb:
            for each_item in rdb.readlines():
                idt,ipt=each_item.rstrip().split(' ')
                result.append(ipt)
    except:
        return []
    else:
        return result

@printer_related_blueprint.route(CONSTS.ROUTES.REQUEST_SET_JOB_TOKEN,methods=['POST'])
@login_required
def UpdatePrinterIP():
    ida=request.args.get('id','')
    ipa=request.args.get('ip','')
    sign=request.args.get('sign','')
    try:
        current_db=[]
        with open('./runtime_ipdb') as rdb:
            for each_item in rdb.readlines():
                idc,ipc=each_item.rstrip().split(' ')
                current_db.append(tuple(idc,ipc))
    except:
        current_db=[]
    for i,each in enumerate(current_db):
        if each[0]==ida:
            current_db[i][1]=ipa
    try:
        with open('./runtime_ipdb','w') as rdb:
            for idc,ipc in current_db:
                print(idc, ipc,sep=' ')
    return None
"""
    #try:
    #    with open('./runtime_ipdb','w') as rdb:
    #        for idc,ipc in current_db:
    #            print(idc,ipc,sep=' ')
    #return None

@printer_related_blueprint.route(CONSTS.ROUTES.STATUS_REPORT,methods=['POST'])
@login_required
def StatusReport():
    response = request.args.get('response', '')
    response = json.loads(response)
    
    toReadableMessage = Template('报告时间：${time} 打印机${name} 位于{geolocation}出现问题：\n{message}')

    nowtime = time.strftime('%Y.%m.%d',time.localtime(time.time()))
    readableMessage = toReadableMessage.safe_substitute(time = nowtime, name = response['name'], geolocation = response['geolocation'], message = response['message'])
    # TODO: Call maintainer
