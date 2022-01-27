########################################### IMPORTS ##################################################


from flask import Blueprint, render_template, request, flash

app_blueprint = Blueprint('app_blueprint',__name__)

from requests.models import Response

import hmac
import hashlib
import base64
import json
import time


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

########################################### LOGIN ROUTES ##################################################

from flask import (
    Flask,
    g,
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
user = {"username": "aaa", "password": "123"}

#Step – 4 (creating route for login)
@app_blueprint.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')     
        if username == user['username'] and password == user['password']:
            
            session.permanent = True
            session['user'] = username
            return redirect('/deposit')
        flash("Login Failed", "info")
        return redirect('/login')

    return render_template("index.html")

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



    
    ########################################################### Binance- API CALLS ###########################################################
import keys

if __name__ == "__main__":
       app_blueprint.run()