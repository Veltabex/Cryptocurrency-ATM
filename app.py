from flask import Flask
from app_blueprint import app_blueprint

if __name__ == '__main__':
    app.run(host='25.76.70.62', port=5000)


app = Flask(__name__)

app.register_blueprint(app_blueprint)
