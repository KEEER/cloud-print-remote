# [In-project modules]
from config import ServerConfig
from utils.logger import initialize_logging_module
# [Python native modules]
import logging
# [Third-party modules]
from flask import Flask,redirect
import waitress

initialize_logging_module()

# don't use __name__ for this one, but for ALL others
main_logger = logging.getLogger('main')

    
server = Flask(__name__)


if __name__ == '__main__':
    # load all blueprints here
    try:
        main_logger.info('All blueprints loaded, server starts up.')
        # start server
        if ServerConfig.debug:
            # use debug server
            server.run(
                host = ServerConfig.host,
                debug = ServerConfig.debug,
                port = ServerConfig.port
            )
        else:
            waitress.serve(
                server,
                host = ServerConfig.host,
                threads = ServerConfig.maximum_threads,
                port = ServerConfig.port
            )
    except Exception as e:
        main_logger.exception('Server crashed.')
        exit()

# 跳转到endpoint完整地址,请修改redirect('***')
# 运行: python3 -m flask run (or type： FLASK_APP=server.py flask run), 
# 在浏览器中测试: http://localhost:5000/
@server.route('/')
def index():
    return redirect('https://github.com')