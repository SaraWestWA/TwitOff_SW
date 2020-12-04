from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(30), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280), nullable=False)  # Tweets are beyond ASCII thus, need Unicode
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    
    def __repr__(self):
        return f'<Tweet: {self.text}'
        

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
 
# DB = SQLAlchemy()


# class User(DB.Model):
#     id = DB.Column(DB.BigInteger, primary_key=True)
#     username = DB.Column(DB.String(80), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username


# class Tweet(DB.Model):
#     id = DB.Column(DB.BigInteger, primary_key=True)
#     text = DB.Column(DB.String(320), nullable=False)
#     user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
#     user = DB.relationship('User', backref=DB.backref('tweet', lazy=True))

#     def __repr__(self):
#         return f'<Tweet: {self.text}>'


# To create the database:
# from twitoff.models import DB, User, Tweet
# DB.create_all()