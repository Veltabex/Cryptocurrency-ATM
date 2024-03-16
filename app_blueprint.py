########################################### IMPORTS ##################################################

import requests
import json
from paytmchecksum import generateSignature
from flask import Blueprint, render_template, request, flash
from keys import merchant_id,merchant_key

app_blueprint = Blueprint('app_blueprint',__name__)

from binance import Client

import json


########################################### IMPORTS END ##################################################

########################################### HTML ROUTES ##################################################

@app_blueprint.route('/coins')
def coins():
    return render_template("coins.html")

@app_blueprint.route('/')
@app_blueprint.route('/home')
def home():
    return render_template("home.html")

@app_blueprint.route('/form', methods = ['POST', 'GET'])
def form():
    return render_template("form.html")

@app_blueprint.route('/buy')
def buy():
    return render_template("buy.html")

@app_blueprint.route('/success')
def success():
    return render_template("success.html")

@app_blueprint.route('/failure')
def failure():
    return render_template("failure.html")

@app_blueprint.route('/failpaytm')
def failpaytm():
    return render_template("faillptm.html")

########################################### LOGIN ROUTES ##################################################

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)

from flask_socketio import SocketIO, emit
from flask_login import current_user, logout_user
from datetime import timedelta

#Step – 1(import necessary library)
from flask import (Flask, render_template, request, redirect, session,flash)

#Step – 2 (configuring your application)
app = Flask(__name__)
app.secret_key = 'ItShouldBeAnythingButSecret'
socketio = SocketIO(app)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 12)

#step – 3 (creating a dictionary to store information about users)
user = {"username": "username", "password": "password"}

#Step – 4 (creating route for login)
@app_blueprint.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method != 'POST':
        return render_template("index.html")
    username = request.form.get('username')
    password = request.form.get('password')
    if username == user['username'] and password == user['password']:

        session.permanent = True
        session['user'] = username
        return redirect('/deposit')
    flash("Login Failed", "info")
    return redirect('/login')

#Step -5(creating route for deposit and logout)
@app_blueprint.route('/deposit')
def deposit():
    if('user' in session and session['user'] == user['username']):
        return render_template("deposit.html")
    

    return '<h1>You are not logged in.</h1>'  

#Step -6(creating route for logging out)

@app_blueprint.route('/logout')
def logout():
    session.pop('username',None)
    flash("You were logged out.", "info")
    return redirect(url_for("app_blueprint.login"))
    
@socketio.on('disconnect')
def disconnect_user():
    logout_user()
    session.pop('ItShouldBeAnythingButSecret', None)


########################################### TEST OR FUNCTION ROUTES #####################################
from keys import api_key, api_secret

client = Client(api_key, api_secret)

########################################################### Binance- API CALLS ###########################################################

def paytm_check_money(order_id,amt):
    print(order_id)
    paytmParams = {
        'body': {
            "mid": merchant_id,
            "orderId": str(order_id)
        }
    }
    checksum = generateSignature(json.dumps(paytmParams["body"]), merchant_key)
    
    paytmParams["head"] = {
        "signature"	: checksum
    }
    
    post_data = json.dumps(paytmParams)
    url = "https://securegw.paytm.in/v3/order/status"
    
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()

    try:
        amt_sent = response['body']['txnAmount']
    except Exception:
        return False
    
    return float(amt_sent)==int(amt)

@app_blueprint.route('/buycrypto',methods=["GET","POST"])
def paytmchecker():
    order_id = request.form['tid']
    amt = request.form['wallet']
    try:
        if paytm_check_money(order_id,amt):
            addr = request.form['Email']
            client.withdraw(
                    coin='USDT',
                    network = 'TRX',
                    address=f'{addr}',
                    amount=amt)

            return redirect(url_for("app_blueprint.success"))
        else:
            return redirect(url_for("app_blueprint.failpaytm"))
    except Exception as e:
        print(e)
        
        return redirect(url_for("app_blueprint.failure"))
        

# ######
# from binance.exceptions import BinanceAPIException
# try:
#     # name parameter will be set to the asset value by the client if not passed
#     result = client.withdraw(
#         coin='USDT',
#         address='<TBZay7hNZT4PwQf3oV7MRpc8RuUTSLLYy2>',
#         amount=2)
# except BinanceAPIException as e:
#     print(e)
# else:
#     print("Success")
#     ####`

# ########################################### IMPORTS ##################################################


# from flask import Blueprint, render_template, request, flash

# app_blueprint = Blueprint('app_blueprint',__name__)

# from requests.models import Response

# import hmac
# import hashlib
# import base64
# import json
# import time


# ########################################### IMPORTS END ##################################################

# ########################################### HTML ROUTES ##################################################

# @app_blueprint.route('/coins')
# def coins():
#     return render_template("coins.html")

# @app_blueprint.route('/')
# @app_blueprint.route('/home')
# def home():
#     return render_template("home.html")

# @app_blueprint.route('/form', methods = ['POST', 'GET'])
# def form():
#     return render_template("form.html")

# @app_blueprint.route('/buy')
# def buy():
#     return render_template("buy.html")

# @app_blueprint.route('/success')
# def success():
#     return render_template("success.html")

# ########################################### LOGIN ROUTES ##################################################

# from flask import (
#     Flask,
#     g,
#     redirect,
#     render_template,
#     request,
#     session,
#     url_for,
#     flash
# )

# from flask_socketio import SocketIO, emit
# from flask_login import current_user, logout_user
# from datetime import timedelta

# #Step – 1(import necessary library)
# from flask import (Flask, render_template, request, redirect, session,flash)

# #Step – 2 (configuring your application)
# app = Flask(__name__)
# app.secret_key = 'ItShouldBeAnythingButSecret'
# socketio = SocketIO(app)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 12)

# #step – 3 (creating a dictionary to store information about users)
# user = {"username": "username", "password": "password"}

# #Step – 4 (creating route for login)
# @app_blueprint.route('/login', methods = ['POST', 'GET'])
# def login():
#     if(request.method == 'POST'):
#         username = request.form.get('username')
#         password = request.form.get('password')     
#         if username == user['username'] and password == user['password']:
            
#             session.permanent = True
#             session['user'] = username
#             return redirect('/deposit')
#         flash("Login Failed", "info")
#         return redirect('/login')

#     return render_template("index.html")

# #Step -5(creating route for deposit and logout)
# @app_blueprint.route('/deposit')
# def deposit():
#     if('user' in session and session['user'] == user['username']):
#         return render_template("deposit.html")
    

#     return '<h1>You are not logged in.</h1>'  

# #Step -6(creating route for logging out)

# @app_blueprint.route('/logout')
# def logout():
#     session.pop('username',None)
#     flash("You were logged out.", "info")
#     return redirect(url_for("app_blueprint.login"))
    
# @socketio.on('disconnect')
# def disconnect_user():
#     logout_user()
#     session.pop('ItShouldBeAnythingButSecret', None)

# ########################################### TEST OR FUNCTION ROUTES #####################################

# from binance.exceptions import BinanceAPIException
# from binance import Client

# api_key = "g257kS41SLmFPNWi1tUaFbPSTjiKYj3Rb1D4kLuHFsgAmsn5FoZ628E6yXvtYaV7"
# api_secret = "935PKy1hPks2MTA5SuItUeB9QT4A2ZFItGySJkyc2wdIkVdos2S0jYNawbH0IjIU"
# client = Client(api_key, api_secret)


# try:
#     # name parameter will be set to the asset value by the client if not passed
#     result = client.withdraw(
#         coin='USDT',
#         network = 'TRX',
#         address= 'TBZay7hNZT4PwQf3oV7MRpc8RuUTSLLYy2',
#         amount=2)
# except BinanceAPIException as e:
#     print(e)
# else:
#     print("Success")

# # return render_template("deposit.html")
    
#     ########################################################### Binance- API CALLS ###########################################################
# import keys

# if __name__ == "__main__":
#        app_blueprint.run()