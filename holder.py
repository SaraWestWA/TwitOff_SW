# export FLASK_APP=twitoff:APP


from flask import Flask
from .db_model import DB, User

def create_app():
    '''Create and configure an instance of the Flask application.'''
    app = Flask(__name__)

    app.config[SQALCHEMY_DATABASE_URI] = 'sqlite:///C:\\Users\\whats\\Repos\\TwitOff_SW\\twitoff.sqlite3' # for absolute path
    app.config[SQALCHEMY_TRACK_MODIFICATIONS] = False
    DB.init_app(app) #connect Flask app to SQAlchemy DB

    @app.route('/')
    def root():
        return 'Welcome to TwitOff!'
    
    # @app.route('<username>/,followers>')
    # def add_users(username, followers):
    #     user = User(username=username, followers=followers)
    #     DB.session.add(user)
    #     DB.session.commit()

    #     return f'{username} has been added to the TwitOff DB!'

    return app

# if __name__ == "__main__":
#     app.run(debug=True)