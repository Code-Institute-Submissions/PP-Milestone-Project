import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm                                                             ## for login & signup forms
from wtforms import StringField, PasswordField, BooleanField                                ## checkboxes & fields
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash                   ## for hiding passowrds in the file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from estimate import estimate_score                                                         ## Assign specific estimators to the given scores


app = Flask(__name__)
app.config['SECRET_KEY'] = 'BiggestSecret'
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


## Survey questions:

Survey = [
{
'question': 'Type of prediction:',
'answers': ['Category', 'Quantity', 'Just looking'], 
},
{

'question': 'Dataset is:', 
'answers': ['Labelled', 'Not labelled'], 
},
{
'question': 'Size of a dataset:', 
'answers': ['Less than 100K samples', 'More than 100K samples'], 
},
{
'question': 'Amount of categories known:', 
'answers': ['Yes', 'No'], 
},
{
'question': 'Data type:', 
'answers': ['Text data', 'Other'],
},

]

    
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
    
## Handle the process of writing data to a file  

def write_to_file(filename, data):    
    with open(filename, "a") as file:
        file.writelines(data)
    

## ROUTES - INDEX (Start Page):

@app.route('/')
def index():
    return render_template('index.html')


## ROUTES - SIGNUP:

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    hashed_password = generate_password_hash(form.password.data, method='sha256')
    if form.validate_on_submit(): 
        write_to_file("data/signup.txt", "Username: " + form.username.data + "\t" + 
                      " | Email: " + form.email.data + "\t" + 
                      " | Password: " + hashed_password + "\n")
        return redirect(url_for('login'))
 
    return render_template('signup.html', form=form)                            ## passing signup form to signup template    


## ROUTES - LOGIN:

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():                                               ## if form was submitted....
        write_to_file("data/login.txt",datetime.now().strftime("%H:%M:%S") + "\t" + form.username.data + "\n")
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', form=form)                             ## passing login form to login template



## ROUTES - DASHBOARD (Survey Form):

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
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
            elif user_answer == 'Yes': 
                score += 10 
            elif  user_answer == 'No':
                score += 20
            elif user_answer == 'Text data': 
                score += 1
            elif  user_answer == 'Other':
                score += 2
            else: 
                score += 0


## Assign specific estimators to the given scores:
        result = estimate_score(score) 

## Pass each estimator as flash message:        
        for element in result:
            flash(element)

        return render_template('results.html')

    return render_template('dashboard.html', questions=Survey)    
    
## To get back to survey from results page:

@app.route('/results', methods=['GET', 'POST'])

def results():
    return render_template('dashboard.html')



## Initiate app

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
            
            