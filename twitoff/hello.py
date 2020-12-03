from flask import Flask, render_template
from .models import DB
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
# from .db_model import DB, User, Tweet
# from .twitter import add_user_tweepy, update_all_users
# from .predict import predict_user
# import traceback

# def create_app():
'''Create and configure an instance of the Flask application.'''
app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL_2'),
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('TRACK_MODS')
    )
DB.init_app(app) #connect Flask app to SQAlchemy DB

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('my_template.html', name=name)

@app.route('/new')
def new():
    return 'Hello, Brave New World!'


if __name__ == "__main__":
app.run(debug=True)