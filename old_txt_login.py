## This is the older signup/login system without SQLAlchemy database implementation




## Handle the process of writing data to a file  

def write_to_file(filename, data):    
    with open(filename, "a") as file:
        file.writelines(data)
        
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
    
    
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():                                               ## if form was submitted....
        write_to_file("data/login.txt",datetime.now().strftime("%H:%M:%S") + "\t" + form.username.data + "\n")
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', form=form)                             ## passing login form to login template    