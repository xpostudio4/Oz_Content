"""Configuration of the application lives here"""
import os
from flask import Flask
from flask.ext.login import LoginManager, UserMixin
from models import db, User
from views import blueprint


STAGE = os.getenv('FLASK_CONFIGURATION_SETTINGS', 'production')

app = Flask(__name__)
app.register_blueprint(blueprint)

app.config['SECRET_KEY'] = 'OzzyContented!$#'

## OAUTH Configuration of the app

app.config['OAUTH_CREDENTIALS'] = {
    'twitter': {
        'id': 'dpuaJM5P9hh6UZ0aPBuDWWg7x',
        'secret' : 'JqeVKjuQycPZaGzxajFdT3OS4WUPzu8odfT8rF66wdOhwA1dWn',
        },
}

if STAGE == 'local':
    #configure local database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ozcontent@127.0.0.1:5432/ozcontent'
    app.debug = True

else:
    #configuration of production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ozcontent@127.0.0.1:5432/ozcontent'


db.init_app(app)
lm = LoginManager(app)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000)
