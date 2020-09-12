from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os
#from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #db object that represents the db object. you create the object by passing it the application

login = LoginManager(app)
login.login_view = 'login' #if user tries to access a page with the @login decorator, the decorator will intercept the request and send the user to the login page.

#migrate = Migrate(app, db) - i skipped this session

if not app.debug:
 
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240000,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')






from app import routes, models, errors