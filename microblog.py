from app import app, db, login
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
    #allows you to run flask shell to run tests on scripts