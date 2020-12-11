'''TwitOff Application'''
import os
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user, update_all_users


def create_app():
    '''Create and configure an instance of the Flask application.'''
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('TRACK_MODS')
        )
    DB.init_app(app)  # connect Flask app to SQAlchemy DB

    @app.route('/')
    def root():
        DB.create_all()
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name='name', message=''):
        name = name or request.values['username']
        try:
            if request.method == 'POST':
                name = request.values['user_name']
                print('Name: ', name)
                if name == '':
                    message = 'Please select or enter a user name.'
                    tweets = []
                else:
                    add_or_update_user(name)
                    message = 'Tweets by {}!'.format(name)
                    tweets = User.query.filter(User.name == name).one().tweets
            else:
                tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f'''Error adding "{name}". Is the name on the user list in
                        any form? Just click it. If not, user may not exist,
                        check spelling and try again.'''
            # message = f'{e}'
            tweets = []

        return render_template('user.html',
                                title=name,
                                tweets=tweets,
                                message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = 'Two different users must be provided to compare!'
        else:
            prediction = predict_user(user1, user2, tweet_text)
            message = f''' "{tweet_text}" is more likely to be said by
                            "{user1 if prediction else user2}"
                            than "{user2 if prediction else user1}""'''

        return render_template('predict.html',
                                title='Prediction',
                                message=message)

    @app.route('/update', methods=['GET'])
    def update():
        update_all_users()
        return render_template('base.html',
                               title='All tweets updated!',
                               users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        # return render_template('base.html', title='Database has been reset!')
        return render_template('base.html',
                               title='Database has been reset!',
                               users=User.query.all())

    return app
