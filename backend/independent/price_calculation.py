# [In-project modules]
from config import endpoint_config
# [Python native modules]
import configparser
import json
from logging import getLogger
# [Third-party modules]


logger = getLogger(__name__)

def calculate_price(config, printer):
    """
    calculate_price
    ===
    This will calculate the price for a configuration on a given printer;

    Return Values on Error
    ---
    | value | description |
    | -1 | page_count exceeds the maximum page limit of the endpoint server. |
    | -2 | Invalid form. |
    """
    global endpoint_config
    try:
        page_count = config.get('page-count', '')
        print_type = 'colored' if config['colored'] else 'normal'
        if page_count == '':
            return -2
        if page_count > endpoint_config[printer]['max_pages']:
            return -1
        else:
            return endpoint_config[printer][print_type][page_count-1]
    except KeyError:
        # double security
        return -2
    except Exception as other_exception:
        logger.exception('<{' + str(other_exception) + '}> happend with config <'+str(config)+'> ')
        return -2