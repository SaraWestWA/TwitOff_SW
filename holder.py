from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(80), unique=True, nullable=False)
    followers = DB.Column(DB.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    tweet = DB.Column(DB.String(280), unique=True, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweet', lazy=True))

    def __repr__(self):
        return '<Tweet %r>' % self.tweet





        # user = User(username=username, followers=followers)
        # DB.session.add(user)
        # DB.session.commit()

        # return f'{username} has been added to the DB!'      


# To create the database:
# from twitoff.db_model import DB, User, Tweet
# DB.create_all()

# Tweet(tweet='Hoomon not shares food. Bad Hoomon!', user=User.query.filter_by(username='JWolf').first())
# User.query.all()
# DB.session.add(tweet2)
# DB.session.commit()


'''Prediction of User authorship based on Tweet Embeddings'''
import numpy as np
from sklearn.linear_model import LogisticRegression
from .db_model import User
from .twitter import nlp, vectorize_tweet
def predict_user(user1, user2, tweet_text):
    '''Determine and return which user is more likely to say a given tweet.
    # Arguments: 
        user1: str, twitter user name for user 1 in comparison from web form
        user2: str, twitter user name for user 2 in comparison from web form
        tweet_text: str, tweet text to evaluate from web form
    # Returns
       predction from logitstic regression model
    '''
    user1 = User.query.filter(User.username == user1).one()
    user2 = User.query.filter(User.username == user2).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweet])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweet])
    # Combine embeddings and create labels
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1_embeddings)),
                             np.zeros(len(user2_embeddings))])
    # Train model and convert input text to embeddings
    log_reg = LogisticRegression(max_iter=1000).fit(embeddings, labels)
    tweet_embedding = vectorize_tweet(nlp, tweet_text)
    return log_reg.predict([tweet_embedding])[0]

          <input id="bmenub" type="checkbox" class="show">
      <label for="bmenub" class="burger pseudo button">Menu</label>
      <div class="menu">
        <a href="/update" class="button warning">Update Tweets</a>
      </div>