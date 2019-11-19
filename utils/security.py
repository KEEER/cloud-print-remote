# [In-project modules]
from config import ServerConfig
# [Python native modules]
import hashlib
# [Third-party modules]
import rsa

# we load the private key here from a pem file
with open('private_key','rb') as fr:
    _keydata = fr.read()
_rsa_private_key = rsa.PrivateKey.load_pkcs1(_keydata)

def kas_sign(value):
    """
    kas_sign
    ====
    Signs information with the KAS standard
    """
    coder = hashlib.sha512()
    coder.update(bytearray(value+ServerConfig.kas_secret_key, encoding='UTF8'))
    return coder.hexdigest()

def cp_sign(value):
    """
    cp_sign
    ===
    Signs information with the Cloud Print standard
    """
    coder = hashlib.sha256()
    coder.update(bytearray(value+ServerConfig.cp_secret_key, encoding='UTF8'))
    return coder.hexdigest()

def secured_sign(value):
    """
    secured_sign
    ===
    Encrypts and signs `value` by private key according to Cloud Print standard.
    """
    global _rsa_private_key
    return rsa.sign(value+ServerConfig.cp_secret_key, _rsa_private_key, 'SHA-256')

