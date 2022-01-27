from flask import Flask
from app_blueprint import app_blueprint

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

app.register_blueprint(app_blueprint)
