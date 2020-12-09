''' Prediction of User authorship based on tweet embeddings'''
import numpy as np
import spacy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import nlp 


def predict_user(user1, user2, tweet_text):
    ''' Determine an return which user is more likely to say a given tweet.

    # Arguments:
        user1: str, twitter user  name for user1 in comparison from web form
        user2: str, twitter user  name for user2 in comparison from web form
        tweet_text: str, tweet text to evaluate from web form

    #Returns
        prediction from logistic regression model
    '''

    user1 = User.query.filter(User.name == user1).one()
    user2 = User.query.filter(User.name == user2).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])

    # Combine embeddings and create labels
    embeddings = np.vstack([user1_embeddings, user2_embeddings]) # X matrix
    labels = np.concatenate([np.ones(len(user1_embeddings)),
                            np.zeros(len(user2_embeddings))]) # y vector

    #Train model and convert input text into embeddings
    log_reg = LogisticRegression(max_iter=1000).fit(embeddings, labels)
    tweet_embedding = nlp (tweet_text).vector
    # knnc = KNeighborsClassifier().fit(embeddings, labels)
    # nlp = spacy.load('en_core_web_lg')
    # tweet_embedding = nlp (tweet_text).vector
    # pred = knnc.predict(tweet_embedding)

    return log_reg.predict([tweet_embedding])[0]
    # return pred



