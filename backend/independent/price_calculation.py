# [In-project modules]

# [Python native modules]
import configparser
import json
# [Third-party modules]

class CONSTS:
    ENDPOINT_CONFIG = 'endpoint.config'
    
endpoint_parser = configparser.ConfigParser()
endpoint_parser.read(CONSTS.ENDPOINT_CONFIG)

endpoint_config = {}
for name, values in endpoint_parser.items():
    endpoint_config.update({ \
        name: { \
			'max_pages': int(values.get('max_pages')),
            'normal': [int(i) for i in values.get('normal').split(',')], 
            'color': [int(i) for i in values.get('color').split(',')] 
        } 
    })


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
        config = json.loads(config)
        page_count = config['page-count']
        print_type = 'colored' if config['colored'] else 'normal'
        if page_count > endpoint_config[printer]['max_pages']:
            return -1
        else:
            return endpoint_config[printer][print_type][page_count-1]
    except KeyError:
        # double security
        return -2