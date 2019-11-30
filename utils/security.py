# [In-project modules]
from config import ServerConfig, remote_private_key, endpoint_public_key
# [Python native modules]
import hashlib
import logging
# [Third-party modules]
import rsa

logger = logging.getLogger(__name__)

def kas_sign(value):
    """
    kas_sign
    ====
    Signs information with the KAS standard
    """
    coder = hashlib.sha512()
    coder.update(bytes(value+ServerConfig.kas_secret_key, encoding='UTF8'))
    return coder.hexdigest()

def cp_sign(value):
    """
    cp_sign
    ===
    Signs information with the Cloud Print standard
    """
    coder = hashlib.sha256()
    coder.update(bytes(value+ServerConfig.cp_secret_key, encoding='UTF8'))
    return coder.hexdigest()

def secured_sign(value):
    """
    secured_sign
    ===
    Encrypts and signs `value` by private key according to Cloud Print standard.
    """
    return rsa.sign(bytes(value+ServerConfig.cp_secret_key, encoding = 'utf8'), remote_private_key, 'SHA-256').hex()

def verify(value, sign):
    try:
        rsa.verify(bytes(value, encoding='utf8'), bytes.fromhex(sign), endpoint_public_key)
    except rsa.VerificationError:
       logger.debug('Invalid sign captured.') 
       return False
    return True