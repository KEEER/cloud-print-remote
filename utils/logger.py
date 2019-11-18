# [In-project modules]
from config import ServerConfig
# [Python native modules]
from logging.handlers import RotatingFileHandler
from logging import FileHandler, Formatter, StreamHandler
import logging
# [Third-party modules]

class CONSTS:
    NORMAL_LOG_HANDLER = 'logs/normal.log'
    IMPORTANT_LOG_HANDLER = 'logs/important.log'
    MAX_BYTES = 4 * 1024 * 1024
    BACKUP_NUMBER = 2

def initialize_logging_module():

    normal_formatter = Formatter('<%(name)s> @ %(asctime)s - %(levelname)s : %(message)s')
    important_formatter = Formatter('[%(processName)s - %(threadName)s] For method %(funcName)s in module %(name)s @ %(asctime)s - %(levelname)s : %(message)s')
    
    screen_handler = StreamHandler()
    screen_handler.setFormatter(normal_formatter)
    screen_handler.setLevel(logging.DEBUG if ServerConfig.debug else logging.INFO)

    normal_file_handler = RotatingFileHandler(
        filename = CONSTS.NORMAL_LOG_HANDLER,
        maxBytes = CONSTS.MAX_BYTES,
        backupCount = CONSTS.BACKUP_NUMBER,
        encoding = 'utf8'
    )
    normal_file_handler.setFormatter(normal_formatter)
    normal_file_handler.setLevel(logging.DEBUG if ServerConfig.debug else logging.INFO)
    
    important_file_handler = FileHandler(CONSTS.IMPORTANT_LOG_HANDLER)
    important_file_handler.setFormatter(important_formatter)
    important_file_handler.setLevel(logging.WARNING)

    logging.basicConfig(
        handlers = [
            screen_handler,
            normal_file_handler,
            important_file_handler
        ],
        level = 0
    )


    