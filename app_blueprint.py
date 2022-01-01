from flask import Blueprint, render_template, request, flash

app_blueprint = Blueprint('app_blueprint',__name__)

from requests.models import Response

import hmac
import hashlib
import base64
import json
import time
import requests

@app_blueprint.route('/coins')
def coins():
    return render_template("coins.html")

@app_blueprint.route('/deposit')
def deposit():
    return render_template("deposit.html")

@app_blueprint.route('/')
@app_blueprint.route('/home')
def home():
    return render_template("home.html")


'''
from dotenv import load_dotenv

load_dotenv()

'''

key = "6d3089ee4d8ccf4d062d85069b6378311cce7b25c8ddb8be"
secret = "02242fac9072ad4077bb1fa623fbf6699b6f43476fbd82a45c5680d6ea4f74eb"


@app_blueprint.route('/usdt')
def coinap():
    # python3
    secret_bytes = bytes(secret, encoding='utf-8')

    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))
    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/users/balances"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json();
    print(data);

    for i in data:
        if i["currency"] == "USDT":
            return i

    return str(i)



if __name__ == "__main__":
    app.run()