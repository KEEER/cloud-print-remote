# [In-project modules]

# [Python native modules]
import configparser
import json
# [Third-party modules]
import rsa

class CONSTS:
    ENDPOINT_CONFIG = 'endpoint.config'
    SERVER_CONFIG = 'server.config'
    
_parser = configparser.ConfigParser()
_parser.read(CONSTS.SERVER_CONFIG)


# server config
class ServerConfig:
    global _parser
    debug = _parser['Server'].getboolean('debug')
    host = _parser['Server'].get('host', '0.0.0.0')
    port = int(_parser['Server'].get('port','5000'))
    maximum_threads = int(_parser['Server'].get('maximum_threads','4'))
    kas_secret_key = _parser['Server'].get('kas_secret_key', '')
    cp_secret_key = _parser['Server'].get('cp_secret_key', '')

class DatabaseConfig:
    global _parser
    database = _parser['Database'].get('database', '')
    user = _parser['Database'].get('user', '')
    host = _parser['Database'].get('host', '')
    password = _parser['Database'].get('password', '')
    port = _parser['Database'].get('port', '')

endpoint_config = {}
with open(CONSTS.ENDPOINT_CONFIG, 'r') as file_reader:
    endpoint_config = json.loads(file_reader.read())
    file_reader.close()
    
# we load the keys here from a pem file
_keydata = None
with open('remote_key.pem','rb') as fr:
    _keydata = fr.read()
    fr.close()
remote_private_key = rsa.PrivateKey.load_pkcs1(_keydata)

_keydata = None
with open('endpoint_key.pem','rb') as fr:
    _keydata = fr.read()
    fr.close()
endpoint_public_key = rsa.PublicKey.load_pkcs1(_keydata)