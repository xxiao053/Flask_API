# import a class Flask
from flask import Flask, render_template, url_for
# create an instance 
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)