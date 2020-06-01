# [In-project modules]
from utils.kas_manager import login
# [Python native modules]

# [Third-party modules]
from flask import Blueprint, request, render_template, redirect

frontend_blueprint = Blueprint('frontend_blueprint', __name__)
class CONSTS:
    class ROUTES:
        Q_AND_A = '/Q-A'
        ADVANCED_TIPS = '/advanced-tips'
        WELCOME = '/welcome'
        
@frontend_blueprint.route(CONSTS.ROUTES.Q_AND_A, methods = ['GET'])
def process_question():
    return render_template('question_and_answers.html')

@frontend_blueprint.route(CONSTS.ROUTES.ADVANCED_TIPS, methods = ['GET'])
def process_advanced_tips():
    return render_template('advanced_tips.html')

@frontend_blueprint.route(CONSTS.ROUTES.WELCOME, methods = ['GET'])
def process_welcome():
    return render_template('welcome.html', LOGIN_URL = login())