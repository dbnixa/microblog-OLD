import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
        #searches for database in the database_url environmental variable, and if that is not set, then in the main directory of the application
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
