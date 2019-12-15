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
    REQUEST_KIUID = 'https://account.keeer.net/api/auth/query_kiuid'
    STATUS = 'status'
    RESULT = 'result'
    OK = 0
    REQUEST_HEADER = {
        'User-agent': 'Mozilla/5.0'
    }
    NAME = '登录 Cloud Print'
    # These two are just demo
    LOGO_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Overwatch_circle_logo.svg/600px-Overwatch_circle_logo.svg.png'
    BACKGROUND_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdREANHAoSAAozc-OTddNReGMM82DBhCmhWXFuKzTREhFw_7MO'
    THEME = 'f57c00'
class FailedToGetKiuidError(Exception):
    pass

logger = logging.getLogger(__name__)

def get_kiuid_by_token(token):
    form = {
        CONSTS.TOKEN: token,
        CONSTS.SIGN: kas_sign(token)
    }
    response = requests.post(
        CONSTS.REQUEST_KIUID, 
        data = form,
        headers = CONSTS.REQUEST_HEADER
    )
    if response.status_code != 200:
        logger.exception('Cannot get kiuid, parameters: %s'%str(form))
        raise FailedToGetKiuidError('Cannot get kiuid, parameters: %s'%str(form))
    response = response.json()
    if response[CONSTS.STATUS] == CONSTS.OK:
        return response[CONSTS.RESULT]
    else:
        logger.warning('An invalid token discovered!')
        return None

def token_is_valid(token):
    form = {
        CONSTS.TOKEN: token,
        CONSTS.SIGN: kas_sign(token)
    }
    response = requests.post(
        CONSTS.REQUEST_KIUID, 
        data = form,
        headers = CONSTS.REQUEST_HEADER
    )
    if response.status_code != 200:
        logger.exception('Cannot examine token, parameters: %s'%str(form))
        raise FailedToGetKiuidError('Cannot examine token, parameters: %s'%str(form))
    response = response.json()
    if response[CONSTS.STATUS] == CONSTS.OK:
        return True
    else:
        logger.warning('An invalid token discovered!')
        return False

def pay(kiuid, amount):
    response = requests.get(
        'https://account.keeer.net/api/pay',
        params = {
            'kiuid': kiuid,
            'amount': amount,
            'sign': kas_sign(kiuid+str(amount))
        },
        headers = CONSTS.REQUEST_HEADER
    )
    if response.status_code != 200:
        raise Exception(response.text,response.status_code)
    response = response.json()
    if response['status'] == 0:
        return True, '成功'
    return False, response['message']


def login():
    return 'https://account.keeer.net/customized-login?name=%s&logo=%s&redirect=%s&background=%s&theme=%s' % (
        CONSTS.NAME,
        CONSTS.LOGO_URL,
        ServerConfig.public_address,
        CONSTS.BACKGROUND_URL,
        CONSTS.THEME
    )