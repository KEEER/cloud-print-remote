# [In-project modules]

# [Python native modules]
import configparser
# [Third-party modules]


_parser = configparser.ConfigParser()
_parser.read('server.config')


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
