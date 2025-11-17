# import a class Flask
from flask import Flask
# create an instance 
app = Flask(__name__)

# route are what we type into our browser to go to different pages
# decoraters are just a way to add additional functionality to existing functions 
# "/" is the root page or home page essentially. But we can also create a "home" page as well
# These two pages are using the same contents  
@app.route("/")
@app.route("/home")
def home(): 
    return "<h1>Home Page<h1>"

@app.route("/about")
def about(): 
    return "<h1>About Page<h1>"

if __name__ == "__main__":
    app.run(debug=True)