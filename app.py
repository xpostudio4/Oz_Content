"""Configuration of the application lives here"""
import os
from flask import Flask
from flask.ext.login import LoginManager, UserMixin
from models import db, User
from views import blueprint


STAGE = os.getenv('FLASK_CONFIGURATION_SETTINGS', 'production')

app = Flask(__name__)
app.register_blueprint(blueprint)

app.config.from_object('config.FinalConfig')

db.init_app(app)
lm = LoginManager(app)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
