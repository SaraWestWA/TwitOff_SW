'''Classes for use in the TwitOff application'''
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    '''Model class contains Twitter users'''
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(30), nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger, nullable=False)

    def __repr__(self):
        return f'<User: {self.name}>'

class Tweet(DB.Model):
    '''Tweet class contains Tweets from Twitter users'''
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(280), nullable=False)
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet: {self.text}'

# To create the database:
# from twitoff.models import DB, User, Tweet
# DB.create_all()
