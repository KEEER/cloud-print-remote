from flask import Blueprint, request
from utils.user_status_detection import login_required


class CONSTS:
    class ROUTES:
        REQUEST_GET_JOB_TOKEN='/_api/printer-ips'
        REQUEST_SET_JOB_TOKEN='/_api/printer-ip'


printer_related_blueprint=Blueprint('printer_related_blueprint',__name__)

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
                print(idc,ipc,sep=' ')
    return None