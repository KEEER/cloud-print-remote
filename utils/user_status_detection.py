# [In-project modules]
from utils.kas_manager import token_is_valid, login
from config import ServerConfig
# [Python native modules]

# [Third-party modules]
from flask import request, redirect, make_response

class CONSTS:
    TOKEN = 'kas-account-token'

def login_required(processing_function):
    """
    login_required
    ===
    This should be used as a decorator after the `route` decorator. \n
    It automatically filters the not-logged in conditions.

    Example
    ```Python
    @xxx_blueprint.route(...)
    @login_required
    def process_yyy():
        # it's safe but plz don't do that;
        #  use `get('kas-account-token', '')` instead.
        token = request.cookies['kas-account-token']
        ...
    ```
    """
    def wrapper(*args, **kwargs):
        if request.cookies.get('kas-account-token', '') == '':
            return redirect(login())
        elif not token_is_valid(request.cookies.get('kas-account-token')):
            response = make_response(redirect(login()))
            if not ServerConfig.debug:
                # in the real server
                response.set_cookie('kas-account-token', '', max_age = 0, domain = '.keeer.net')
            else:
                response.set_cookie('kas-account-token', '', max_age = 0)
            return response
        return processing_function(*args, **kwargs)
    wrapper.__name__ = processing_function.__name__
    return wrapper
