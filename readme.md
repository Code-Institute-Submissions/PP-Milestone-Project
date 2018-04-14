# ML Selector Project

## Heroku:
https://mlselector.herokuapp.com/

## Project Case:

How do I know which method of parameter estimation to choose? <br>

It's hard to decide if you have so many different algorithms to your disposal. But with certain information given about analysed dataset, we can narrow that choice to few best matches.


## Goal Statement:
Goal of the project is to create survey, that will help to decide which ML algorithm is the most suitable one for a given task.

## Project Requirements:
1.	Application must enter their answers & submit it using form.
2.	Suggested algorithms and descriptions(instead of q & a) are stored and accessible (MongoDB)
2.	Users have to be identifiable by unique username/password (SqlAlchemy database has been implemented)
3.	App must be written in Python. HTML, CSS, and JavaScript
4.	App should be built with TDD approach
5.	Flask framework should be used 
6.	App should be responsive
7.	Apply Responsive Design


## Test Suite:

### Login/Signin Form Test:
1. Is data properly saved in database
2. Are different templates properly routing to signup and login urls
3. Are form fields values properly validated (example: email field)
4. Is password properly hashed

### Score assigner:
1. Is correct score assign to certain answer
2. If no answer is marked then survey result should be "Please answer all the questions"

### Estimate.py
1. Standard assertion tests within file 

### Data-Questions:
1. Are data questions properly displayed

### Results:
1. Are estimator field properly displayed

### Add suggestion
1. Testing various inputs and datatable functionality

### App Responsivity: 
1. Done with Inspect element tool as a last part of the test suite




## Tools, Modules and Techniques:

Python:<br>
https://www.python.org/

Flask:<br>
http://flask.pocoo.org/

HTML:<br>
https://www.w3schools.com/html/

CSS:<br>
https://www.w3schools.com/css/

Bootstrap:<br>
https://getbootstrap.com/

Materialize:<br>
http://materializecss.com/

FontAwesome:<br>
https://fontawesome.com/

Material Icons:<br>
https://material.io/icons/

Google Fonts (Roboto)<br>
https://fonts.google.com/specimen/Roboto?selection.family=Roboto

JS:<br>
https://www.w3schools.com/js/

SQLite<br>
https://www.sqlite.org/index.html

MongoDB mLab<br>
https://mlab.com

## scikit-learn source

http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html


Thank you,

Lukasz Malucha