from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from wtforms.validators import ValidationError
from flask_login import current_user, login_user
from flask_login import login_required
from flask import request
from flask_login import logout_user
from app.models import User
from app import db
from app.forms import RegistrationForm, EditProfileForm
from datetime import datetime



@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Home', posts=posts)#inside of index.html, there is a call to 'extend' the base class, so the base class is imported essentially into index.html 


@app.route('/login', methods=['GET', 'POST'])
def login():
    #redirect any user who is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #instantiate the form class we created and send it as an argument to renter_template below so that user sees the form
    form = LoginForm()
    #if the user enters valid information:
    if form.validate_on_submit():
        #run a db query for user information provided and initialize a variable with the result. 
        user = User.query.filter_by(username=form.username.data).first()
        #if result of db query is none or the password isn't valid, then flask invalid username/password and redirect the user back to the login() function via url_for
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        #if username and password match, then login user and redirect to index function. This creates cookie and session
        login_user(user, remember=form.remember_me.data)
        
        #see commend in __init__.py. this handles sending the user back to the page they tried to access after entering their password. It processes the next argument that gets inserted into the query string by the decorator. 
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index')) 



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit(): #validation takes place in form.py.
        user = User(username=form.username.data, email=form.email.data)#user = result of database call.
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('you have successfully registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
#Flask will accept any text in the dynamic of the URL, and will invoke the view function with the actual text as an argument.
@login_required
def user(username):
    #check if user exists. If not, surface 404 error to client. If yes, then initialize posts variable and render 'user.html'
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():

        if form.username.data != current_user.username:
            new_user_name = form.username.data
            user = User.query.filter_by(username=new_user_name).first()
            if user is not None:
                flash('User name already take. Please choose a different name.')
                #raise ValidationError('Please use a different username.')
                return redirect(url_for('edit_profile'))
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()#not sure how this saves the current_user... is the current_user always 'added' and just needs to be committed to be saved? What's the difference between added and commited?
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)