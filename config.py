"""Configuration file of the project"""
import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://ozcontent@127.0.0.1:5432/ozcontent'

    OAUTH_CREDENTIALS = {
    'twitter': {
        'id': 'dpuaJM5P9hh6UZ0aPBuDWWg7x',
        'secret' : 'JqeVKjuQycPZaGzxajFdT3OS4WUPzu8odfT8rF66wdOhwA1dWn',
        },
    }

    SECRET_KEY = 'OzzyContented!$#'

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://ufcofxthphdbga:gaXaZs-830eOTtM8a7YccAqnTX@ec2-107-22-187-89.compute-1.amazonaws.com:5432/de0jhotbsj3mbq'


STAGE = os.getenv('FLASK_CONFIGURATION_SETTINGS', 'production')


if STAGE == 'local':
    FinalConfig = Config
else:
    FinalConfig = ProductionConfig
