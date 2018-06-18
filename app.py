import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm                                                             ## for login & signup forms
from wtforms import StringField, PasswordField, BooleanField                                ## checkboxes & fields
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash                   ## for hiding passowrds in the file
from flask_login import LoginManager,login_user, login_required, logout_user, current_user, UserMixin, AnonymousUserMixin
from estimate import estimate_score                                                         ## Assign specific estimators to the given scores
from flask_sqlalchemy import SQLAlchemy

from flask_pymongo import PyMongo
from bson.objectid import ObjectId


############################################################################ App Foundations #################################################################################################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BiggestSecret'
## For User Credentials:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
## For Suggested Questions:
app.config["MONGO_DBNAME"] = 'q_and_a'
app.config["MONGO_URI"] = 'mongodb://practicepython:codeinstitute@ds227035.mlab.com:27035/q_and_a'

Bootstrap(app)
db = SQLAlchemy(app)
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ## Test config
# class TestConfig():
#     DEBUG = True
#     TESTING = True
#     WTF_CSRF_ENABLED = False
#     SECRET_KEY = 'BiggestSecret'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///testdatabase.db'



## Create database for Users

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
## Initiate Guest User    
    
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'
    
    
login_manager.anonymous_user = Anonymous
    
## Login Form

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('Remember Me')

## Register Form

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Please enter correct email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    


############################################################################ ML Selector #################################################################################################################################

## ROUTES - DASHBOARD:

@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    questions=mongo.db.Questions.find()
    result = []
    message = 'Please answer all the questions'
    if request.method == 'POST':
        score = 0 
        answers = request.form 

## Assign score to the given asnwer:        
        for question, user_answer in answers.items():
            if user_answer == 'Category': 
                score += 10000
            elif  user_answer == 'Quantity':
                score += 20000
            elif  user_answer == 'Just looking':
                score += 30000    
            elif user_answer == 'Labelled': 
                score += 1000 
            elif  user_answer == 'Not labelled':
                score += 2000    
            elif  user_answer == 'Less than 100K samples':
                score += 100
            elif  user_answer == 'More than 100K samples':
                score += 200   
            elif user_answer == 'Known': 
                score += 10 
            elif  user_answer == 'No idea':
                score += 20
            elif user_answer == 'Text data': 
                score += 1
            elif  user_answer == 'Other':
                score += 2
            else: 
                score += 0


## Assign specific estimators to the given scores:
        result = estimate_score(score) 
        message = 'Suggested Machine Learning algortihms are:' 
## Pass each estimator as flash message:        
        for element in result:
            flash(element)
           
        
    return render_template('dashboard.html', questions=questions, result = result, user = current_user.username, message = message)    


####################################################################### Adding algorithms ################################################################################################################################


## ROUTES - Suggest Algorithm:

@app.route('/add_algorithm')
def add_algorithm():
    suggested_algorithms = mongo.db.suggested_algorithms.find()
    return render_template('add_request.html', suggested_algorithms = suggested_algorithms, user = current_user.username)


## ROUTES - Save Algorithm:

@app.route('/insert_algorithm', methods=['POST'])
def insert_algorithm():
    suggested_algorithms =  mongo.db.suggested_algorithms
    suggested_algorithms.insert_one(request.form.to_dict())
    return redirect(url_for('add_algorithm'))
    
## ROUTES - Delete Algorithm:    
    
@app.route('/delete_algorithm/<algorithm_id>')
def delete_algorithm(algorithm_id):
    mongo.db.suggested_algorithms.remove({'_id': ObjectId(algorithm_id)})
    return redirect(url_for('add_algorithm'))    
    
    
## ROUTES - SciKit Map:      

@app.route('/fullmap')
def full_map():
    return render_template('map.html', user = current_user.username)


##################################################################### User Handling ######################################################################################################################################



## ROUTES - SIGNUP:

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    hashed_password = generate_password_hash(form.password.data, method='sha256')           ## password get hashed for security purposes
    if form.validate_on_submit(): 
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
 
    return render_template('signup.html', form=form)                            ## passing signup form to signup template    


## ROUTES - LOGIN:

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():                                               ## if form was submitted....
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        
        return '<h1>Invalid username or password</h1>'         
    
    return render_template('login.html', form=form)                             ## passing login form to login template


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    
    
@app.errorhandler(404)
def error404(error):
    return render_template('404.html')
    
@app.errorhandler(500)
def error500(error):
    return render_template('500.html')

## Initiate app

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
debug=False)