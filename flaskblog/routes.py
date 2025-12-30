from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, engine, bcrypt, db 
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from sqlalchemy import text
from flaskblog.models import sql_insert_user
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm() 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  
        # hash user's pwd and only store hashed pwd; with .decode() we get hashed string instead byte version
        with engine.begin() as conn: 
            conn.execute(text(sql_insert_user), {"username":form.username.data, "email":form.email.data, "password":hashed_password})
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))  
    # url_for(xxx ) xxx is the func name, not the route name; return the url of corresponding route
    return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['Get', 'POST'])
def login():
    if current_user.is_authenticated:
        # when user login successfully, remove login and register, logout appears 
        return redirect(url_for('home'))
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # check if user enter an email exists in db
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # if user enter pwd is valid based on hashed pwd in db
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # actually redirect user to the page user visited (before being directed to login page)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required  # you have to login to access this page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title='Account', image_file=image_file, form=form)  # pass value to template throng params