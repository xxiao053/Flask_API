from flask import render_template, url_for, flash, redirect 
from flaskblog import app, engine, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from sqlalchemy import text
from flaskblog.models import sql_insert_user

posts = [
    {
        'author': 'Xiao Xiao',
        'title': 'First Blog Post',
        'content': 'This is the first post content',
        'date_posted': 'Sep 20, 2025'
    },
    {
        'author': 'Sean James',
        'title': 'What Makes You a Better Developer',
        'content': 'When people first learn programming, they often focus on writing scripts, solving LeetCode problems, or building simple web pages. APIs feel like something “big companies” use. But the truth is: learning how to build even a basic API instantly levels up how you think about software.',
        'date_posted': 'Oct 21, 2025'
    },
    {
        'author': 'Martine Harden',
        'title': "It's the foundation of almost every modern system",
        'content': 'Payments, messaging apps, social networks, e-commerce—everything runs on APIs.\n\nEven inside Meta, Google, or PayPal, teams talk to each other through internal APIs every day.\nOnce you understand APIs, you understand how large systems communicate.',
        'date_posted': 'Nov 29, 2025'
    },
]

# route are what we type into our browser to go to different pages
# decoraters are just a way to add additional functionality to existing functions 
# We use the route() decorator to tell Flask what URL should trigger our function.
# "/" is the root page or home page essentially. But we can also create a "home" page as well
# These two pages are using the same contents  
@app.route("/")
@app.route("/home")
def home(): 
    return render_template("home.html", posts=posts)  
# all html files must be stored under the "templates" folder, and it render html files
# pass variable into html  

@app.route("/about")
def about(): 
    return render_template("about.html", title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm() 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        with engine.begin() as conn: 
            conn.execute(text(sql_insert_user), {"username":form.username.data, "email":form.email.data, "password":hashed_password})
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))  
    # url_for(xxx) xxx is the func name, not the route name; return the url of corresponding route
    return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['Get', 'POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home')) 
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title='Login', form=form)