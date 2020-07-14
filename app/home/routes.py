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

    Positive = 10
    Netural = 10
    Negative = 10

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

    data = "My Name is Shubsdfghjkwhdc wudiwuddad ksd ham Kondekar Kondekar Kondekar"

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

@blueprint.route('/barchart',methods=["GET","POST"])
def barchart():
    # Positive = [ele1,ele2,ele3,ele4,ele5]
    # Neutral = [ele1,ele2,ele3,ele4,ele5]
    # Negative = [ele1,ele2,ele3,ele4,ele5]

    # data = [Positive,Neutral,Negative]

    data = [[3,2,3,4,5],[5,6,1,2,3],[1,5,9,8,3]]
    
    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response