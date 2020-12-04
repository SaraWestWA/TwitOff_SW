from flask import Flask, render_template
from .models import DB

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite'
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to Twitoff'

   @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Database has been reset!', users=User.query.all())

    @app.route('/users/')
    def users(name=None):
        DB.create_all()
        users = User.query.all()
        return render_template('base.html', title='Users Added', users=users)
    
    return app