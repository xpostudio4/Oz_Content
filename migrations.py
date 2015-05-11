import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__)
STAGE = os.getenv('FLASK_CONFIGURATION_SETTINGS', 'production')

if STAGE == 'local':
    #configure local database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ozcontent@127.0.0.1:5432/ozcontent'
    app.debug = True
else:
    #configuration of production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ozcontent@127.0.0.1:5432/ozcontent'

db = SQLAlchemy(app)

from models import *

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()


