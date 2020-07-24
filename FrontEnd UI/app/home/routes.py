# -*- encoding: utf-8 -*-
from app.home import blueprint
from flask import render_template, redirect, url_for,make_response
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from random import random
import json
import time

import re
import mysql.connector
import pandas as pd
import datetime
import collections
count=0

@blueprint.route('/index')
def index():
    return render_template('index.html')

@blueprint.route('/<template>')
def route_template(template):
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
    conn = mysql.connector.connect(
    host="", # Enter the host name
    user="", # Enter the user
    password="", # Enter the password
    database="", # Enter the database name
    charset ='utf8'
)

    query = "SELECT id_str, text, created_at, sentiment, user_location, user_followers_count FROM {}".format("covid19")
    df = pd.read_sql(query, con=conn)
    df['created_at'] = pd.to_datetime(df['created_at']).apply(lambda x: x + datetime.timedelta(hours=5,minutes=30))
    result = df.groupby([pd.Grouper(key='created_at', freq='600s'), 'sentiment']).count().unstack(fill_value=0).stack().reset_index()
    result = result.rename(columns={"id_str": "Num of '{}' mentions".format('#covid'), "created_at":"Time"})

    Positive = result.tail(4).iloc[0]["Num of '#covid' mentions"]
    Netural = result.tail(5).iloc[0]["Num of '#covid' mentions"]
    Negative = result.tail(6).iloc[0]["Num of '#covid' mentions"]

    data = [int(Positive), int(Netural), int(Negative)]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'
    conn.close()

    return response

@blueprint.route('/data', methods=["GET", "POST"])
def data():
    global count
    # Data Format
    # [TIME, Positive, Netural, Negative]
    conn = mysql.connector.connect(
    host="", # Enter the host name
    user="", # Enter the user
    password="", # Enter the password
    database="", # Enter the database name
    charset ='utf8'
)

    query1 = "SELECT time,positive,neutral,negative FROM {}".format("pastdata")
    query2 = "SELECT sentiment FROM covid19"
    df1 = pd.read_sql(query1, con=conn)
    df2 = pd.read_sql(query2, con=conn)

    totPos = df2.sentiment.value_counts()[1]
    totNeu = df2.sentiment.value_counts()[0]
    totNeg = df2.sentiment.value_counts()[-1]
    totTweet = totPos + totNeu + totNeg
    t = df1.iloc[-1]["time"] + 19860000
    Positive = df1.iloc[-1]["positive"]
    Neutral = df1.iloc[-1]["neutral"]
    Negative = df1.iloc[-1]["negative"]

    data = [t, int(Positive), int(Neutral), int(Negative),int(totPos),int(totNeu),int(totNeg),int(totTweet)]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'
    conn.close()
    count+=1

    return response

@blueprint.route('/words', methods=["GET", "POST"])
def wordsdata():
    conn = mysql.connector.connect(
    host="", # Enter the host name
    user="", # Enter the user
    password="", # Enter the password
    database="", # Enter the database name
    charset ='utf8'
)

    query = "SELECT clean_tweet FROM {}".format("covid19")
    df = pd.read_sql(query, con=conn)
    data = " ".join(df['clean_tweet'].tolist()).split()
    n_print = 200
    word_counter = collections.Counter(data)
    list_=[]
    for word, count in word_counter.most_common(n_print):
        list_ = list_ + [word] * count

    data = " ".join(list_)
    response = make_response(json.dumps(data))

    response.content_type = 'application/json'
    conn.close()

    return response

@blueprint.route('/past', methods=["GET", "POST"])
def pastdata():
    conn = mysql.connector.connect(
    host="", # Enter the host name
    user="", # Enter the user
    password="", # Enter the password
    database="", # Enter the database name
    charset ='utf8'
)
    
    query = "SELECT time,positive,neutral,negative FROM {}".format("pastdata")
    df = pd.read_sql(query, con=conn)

    data = []
    for i in range(19):
        data.append(df.iloc[i]["time"]+19860000)
        data.append(int(df.iloc[i]["positive"]))
        data.append(int(df.iloc[i]["neutral"]))
        data.append(int(df.iloc[i]["negative"]))
    
    response = make_response(json.dumps(data))

    response.content_type = 'application/json'
    conn.close()

    return response