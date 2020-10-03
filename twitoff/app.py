from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from .db_model import DB, User, Tweet

# DB=SQLAlchemy()
load_dotenv()

def create_app():
    '''Create and configure an instance of the Flask application.'''
    app = Flask(__name__, instance_relative_config=False)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('TRACK_MODS')
    )

    DB.init_app(app) #connect Flask app to SQAlchemy DB

    @app.route('/')
    def root():
        return render_template('base.html', title='Home',users=User.query.all())
        # return 'Twitoff!'

    @app.route('/<username>/<followers>')
    def add_user(username, followers):
        user = User(username=username, followers=followers)
        DB.session.add(user)
        DB.session.commit()

        return f'{username} has been added to the DB!'

    # @app.route('/tweet/<user_id>/<tweet>')
    # def add_tweet(user_id, tweet):
    #     tweet = Tweet(user_id=user_id, tweet=tweet)
    #     DB.session.add(tweet)
    #     DB.session.commit()

    #     return f'{user} tweeted {tweet}.'

    return app
# if __name__ == "__main__":
#     app.run(debug=True)