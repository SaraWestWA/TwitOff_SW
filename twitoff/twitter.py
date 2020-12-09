import spacy
import tweepy
from decouple import config
from .models import DB, User, Tweet

TWITTER_CONSUMER_KEY = config('TWITTER_CONSUMER_API_KEY')
TWITTER_CONSUMER_SECRET = config('TWITTER_CONSUMER_API_SECRET')
TWITTER_ACCESS_TOKEN = config('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = config('TWITTER_ACCESS_TOKEN_SECRET')

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
TWITTER_AUTH.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

spacy_model_name = "en_core_web_lg"
if not spacy.util.is_package(spacy_model_name):
	spacy.cli.download(spacy_model_name)

nlp = spacy.load(spacy_model_name)
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

def add_or_update_user(name):
    """
    Add or update user and their tweets.
    Throw error if user doesn't exist or is private
    """
    try:
        twitter_user = TWITTER.get_user(name)
        db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, name=name)
        tweets = twitter_user.timeline(count=200,
                                        exclude_replies=True,
                                        include_rts=False,
                                        since_id=db_user.newest_tweet_id)
            
        if tweets:
            db_user.newest_tweet_id = tweets[0].id # Add newest_tweet_id to the User table

        for tweet in tweets:
            embedding = list(nlp(tweet.text).vector)
            db_tweet = Tweet(id=tweet.id, text=tweet.text, embedding=embedding)
            db_user.tweets.append(db_tweet)
        
        DB.session.add(db_user)
        DB.session.commit()

    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        # raise e
