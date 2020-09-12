from app import db
from app import login
#db is the sqlAlchemy db object created in init
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5



@login.user_loader
def load_user(id):
    return User.query.get(int(id))  #This callback is used to reload the user object from the user ID stored in the session cookie. this associates the user_id in the cookie with the user object

class User(UserMixin, db.Model):#1
    #2 class variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic') #posts is not a field on the database, but rather a 'virtual field'.
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'  
        #note - username is a class variable and thus can be accessed by any class method, here __repr__. Note it is not passed as an argument to __repr__. so 'self' means class instance, and username means the class variable

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=mp&s={}'.format(
            digest, size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)



#create database in flask shell:
#>>> from app import db
#>>> db.create_all()




#1 class User inherits from db.Model, which is a base class for all models from Flask SQLAlchemy. 

# 2These class variables are created as instances of the db.Column class, which takes the field type as an argument, plus other optional arguments that provide information about the fields. 

#For a one-to-many relationship, a db.relationship field is normally defined on the "one" side, and is used as a convenient way to get access to the "many". So for example, if I have a user stored in u, the expression u.posts will run a database query that returns all the posts written by that user. The first argument to db.relationship is the model class that represents the "many" side of the relationship. This argument can be provided as a string with the class name if the model is defined later in the module. The backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. This will add a post.author expression that will return the user given a post. The lazy argument defines how the database query for the relationship will be issued

#from sqlAlchemy docs ... the relationship.backref keyword is merely a shortcut for building two individual relationship() constructs that refer to each other. 

#note: the backref='author' argument defines a field that will be added to the objects of the 'many' class that points back at the 'one'. so if u is a user, then u.posts will run a query for all posts by that user, and it will add a post.author expression that will return the user to a givne post.

# Process for creating users in the interpreter. Need to figure out why tutorial doesn't say use create_all... that was necessary. I think it's b/c they create the tables in the migration. 



