# -*- encoding: utf-8 -*-
from app.home import blueprint
from flask import render_template, redirect, url_for,make_response
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from random import random
import json
import time

@blueprint.route('/index')
@login_required
def index():
    
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    return render_template('index.html')

@blueprint.route('/<template>')
def route_template(template):

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    try:

        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500


@blueprint.route('/dataPiecha', methods=["GET", "POST"])
def dataPie():
    # Data Format
    # [Positive, Netural, Negative]

    Positive = 68
    Netural = 45
    Negative = 92

    data = [Positive, Netural, Negative]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

@blueprint.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Positive, Netural, Negative]

    Positive = random() * 100
    Netural = random() * 55
    Negative = random() * 67

    data = [time.mktime(time.gmtime()) * 1000, Positive, Netural, Negative]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

@blueprint.route('/words', methods=["GET", "POST"])
def wordsdata():

    data = "High profile international sporting events such Olympics or World Cups well international religious events such Hajj count mass gatherings. However, lower profile conferences and events can also meet WHO’s definition mass gathering. An event counts mass gatherings if number people it brings together so large that it has potential to strain planning and response resources health system community where it takes place. You need to consider location and duration event well number participants. For example, if event takes place over several days small island state where capacity health system quite limited then even an event with just few thousand participants could place big strain on health system and then be considered mass gathering event. Conversely, if event held big city country with large, well-resourced health system and lasts just few hours, event may not constitute mass gathering event."

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

