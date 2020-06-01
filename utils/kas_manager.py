# [In-project modules]
from utils.security import kas_sign
from config import ServerConfig
# [Python native modules]
import requests
import logging
# [Third-party modules]

class CONSTS:
    TOKEN = 'token'
    SIGN = 'sign'
    REQUEST_BASE = 'https://account.keeer.net/api'
    STATUS = 'status'
    RESULT = 'result'
    OK = 0
    REQUEST_HEADER = {
        'User-agent': 'Mozilla/5.0'
    }
    NAME = '登录 Cloud Print'
    # These two are just demo
    LOGO_URL = ServerConfig.public_address + '/static/img/logo.png'
    BACKGROUND_URL = ServerConfig.public_address + '/static/img/background.webp'
    THEME = 'f57c00'
class FailedToGetKiuidException(Exception):
    pass

logger = logging.getLogger(__name__)

def _construct_get_kiuid_url(token):
    return CONSTS.REQUEST_BASE + '/%s/kiuid' % token

def _construct_rs_header():
    rs_header = {'Authorization': 'Bearer %s' % ServerConfig.kas_service_token}
    rs_header.update(CONSTS.REQUEST_HEADER)
    return rs_header

def _construct_pay_url():
    return CONSTS.REQUEST_BASE + '/pay'

def get_kiuid_by_token(token):
    logger.debug('called kas')
    logger.debug('send request %s with header %s'%(_construct_get_kiuid_url(token), _construct_rs_header()))
    response = requests.get(
        _construct_get_kiuid_url(token), 
        headers = _construct_rs_header()
    )
    logger.debug('recieved request')
    logger.debug('Response: <%s>'%str(response))
    
    if response.status_code != 200:
        logger.exception('Cannot get kiuid, parameters: %s'%str((response.status_code, response.text)))
        raise FailedToGetKiuidException('Cannot get kiuid')
    
    logger.debug('[node-kas test] Kiuid fetched: %s'%response.text)
    response = response.json()
    if response[CONSTS.STATUS] == CONSTS.OK:
        logger.debug('returning: %s'% response[CONSTS.RESULT])
        return response[CONSTS.RESULT]
    else:
        logger.warning('An invalid token discovered!')
        return None

def token_is_valid(token):
    kiuid = None
    logger.debug('called')
    try:
        kiuid = get_kiuid_by_token(token)
        logger.debug('Kiuid gotten: %s'%kiuid)
    except FailedToGetKiuidException as e:
        logger.debug('Token <%s> is not valid as it cannot be used to get kiuid.'%token)
        return False
    finally:
        if kiuid == None:
            # still, not valid
            logger.debug('Token <%s> is not valid as it returned a null.'%token)
            return False
        return True

def pay(kiuid, amount):
    response = requests.post(
        _construct_pay_url(),
        data = {
            'type': 'kiuid',
            'identity': kiuid,
            'amount': amount
        },
        headers = _construct_rs_header(),
    )
    if response.status_code != 200:
        raise Exception(response.text,response.status_code)
    response = response.json()
    logger.debug('Pay response: %s'%response)
    if response['status'] == 0:
        return True, '成功'
    
    # build message
    message = response.get('message', '无响应信息')
    if response['status'] == 3:
        message = '非法数值'
    elif response['status'] == 4:
        message = '您的 Kredit 余额不足'

    return False, message

def get_kredit_amount(token):
    response = requests.get(
        CONSTS.REQUEST_BASE + '/user-information',
        cookies = {'kas-account-token': token},
        headers = CONSTS.REQUEST_HEADER
    )
    if response.status_code != 200:
        raise Exception(response.text,response.status_code)
    response = response.json()
    logger.debug('Kredit fetch response: %s'%response)
    return response.get('kredit', 0)
def login():
    # TODO
    return 'https://account.keeer.net/login?service=cloud-print'
    # 'https://account.keeer.net/customized-login?name=%s&logo=%s&redirect=%s&background=%s&theme=%s' % (
    #     CONSTS.NAME,
    #     CONSTS.LOGO_URL,
    #     ServerConfig.public_address,
    #     CONSTS.BACKGROUND_URL,
    #     CONSTS.THEME
    # )