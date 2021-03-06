# [In-project modules]
from utils.logger import initialize_logging_module
initialize_logging_module() # has to break the rule here otherwise the logging module won't work

from config import ServerConfig
from backend.account_related.account_related_blueprint import account_related_blueprint
from backend.independent.independent_blueprint import independent_blueprint
from backend.printer_related.printer_related_blueprint import printer_related_blueprint
from frontend.frontend_blueprint import frontend_blueprint
from frontend.admin.admin_blueprint import admin_blueprint
# [Python native modules]
import logging
# [Third-party modules]
from flask import Flask
import waitress



# don't use __name__ for this one, but for ALL others
main_logger = logging.getLogger('main')

from utils.json_logger import JSONLogger

lgr = JSONLogger('logs/print_data.log')
lgr.write({'use': False})
if __name__ == '__main__':
    
    server = Flask(__name__)
    # load all blueprints here

    server.register_blueprint(account_related_blueprint)
    server.register_blueprint(independent_blueprint)
    server.register_blueprint(printer_related_blueprint)
    server.register_blueprint(frontend_blueprint)
    server.register_blueprint(admin_blueprint)
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