# [In-project modules]
from utils.kas_manager import pay, get_kiuid_by_token
# [Python native modules]
import logging
# [Third-party modules]
from flask import Blueprint, request, render_template, redirect

admin_blueprint = Blueprint('admin_blueprint', __name__)
logger = logging.getLogger(__name__)

def _write_line(text, newline):
    text += ' \n' + newline
    return text
@admin_blueprint.route('/run-test', methods=['GET'])
def process_run_rest():
    report = ''
    _write_line(report, 'Test begins: trying payment method by paying 0.01 Kredit')
    logger.debug('Test begins: trying payment method by paying 0.01 Kredit')
    result = pay(
        get_kiuid_by_token(request.cookies.get('kas-account-token', '')),
        10
    )
    _write_line(report, 'Result: <%s>'%str(result))
    logger.debug('Result: <%s>'%str(result))
    return '''
    <html>
    <body>
    %s
    </body>
    </html>
    '''%report