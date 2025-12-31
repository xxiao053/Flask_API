import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, engine, bcrypt, db 
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from sqlalchemy import text
from flaskblog.models import sql_insert_user
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home(): 
    page = request.args.get('page', 1, type=int)  # get page #
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page= page, per_page=5)  # pagination 
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)  # the file name when user upload their picture
    picture_fn = random_hex + f_ext  # hash the original file name to avoid potential filename conflict in DB
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)  # resize picture, mitigate server load
    i.save(picture_path)
    prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(prev_picture) and current_user.image_file != 'default.jpg':
        os.remove(prev_picture)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required  # you have to login to access this page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # return hashed filename
            current_user.image_file = picture_file
            print("\n\n\nasd\n\n\n")
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()  # without this, no change save in db 
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title='Account', image_file=image_file, form=form)  # pass value to template throng params

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  # author is the backref, check models.user for details
        db.session.add(post)  # add record to db (=insert into)
        db.session.commit()  # save change
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                            form=form, legend='New Post')

@app.route("/post/<int:post_id>")  # include variable in the route, where id essentially is part of the route
def post(post_id):
    post = Post.query.get_or_404(post_id)  # give me the post with this id, if doesn't exist then return 404
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  
    if post.author != current_user:
        abort(403)  # forbidden
    form = PostForm()
    if form.validate_on_submit():  # when user hit the submit button 
        post.title = form.title.data 
        post.content = form.content.data # change db data, so no need db.session.add
        db.session.commit()  # save change
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete",  methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  
    if post.author != current_user:
        abort(403)  # forbidden
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))