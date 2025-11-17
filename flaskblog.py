# import a class Flask
from flask import Flask, render_template, url_for, flash, redirect 
from forms import RegistrationForm, LoginForm 

# create an instance 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'c765149c9618cedc66ff06f71b2fc50f' # protect our sever from attack 

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

# route are what we type into our browser to go to different pages
# decoraters are just a way to add additional functionality to existing functions 
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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  
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

if __name__ == "__main__":
    app.run(debug=True)