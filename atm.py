from flask import Flask, render_template, request, flash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

import hmac
import hashlib
import base64
import json
import time
import requests

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
key = "6d3089ee4d8ccf4d062d85069b6378311cce7b25c8ddb8be"
secret = "02242fac9072ad4077bb1fa623fbf6699b6f43476fbd82a45c5680d6ea4f74eb"

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

for item in response:
    print(f"Currency: {item['currency']} | Balance: {item['balance']}")
