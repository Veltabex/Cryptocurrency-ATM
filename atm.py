import hmac
import json
import time
import base64
import hashlib
import requests
from flask import Flask, render_template, request, flash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

key = "6d3089ee4d8ccf4d062d85069b6378311cce7b25c8ddb8be"
secret = "02242fac9072ad4077bb1fa623fbf6699b6f43476fbd82a45c5680d6ea4f74eb"
secret_bytes = bytes(secret, encoding='utf-8')
timeStamp = int(round(time.time() * 1000))

body = {
    "timestamp": timeStamp
}

json_body = json.dumps(body, separators = (',', ':'))
signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
}

response = requests.post("https://api.coindcx.com/exchange/v1/users/balances", data = json_body, headers = headers)
data = response.json();
print(data);

for item in response:
    print(f"Currency: {item['currency']} | Balance: {item['balance']}")
