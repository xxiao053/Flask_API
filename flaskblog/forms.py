from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 
    # design the form and validation  
    # create a string field for username, cannot be empty, and length between 2 and 20 char
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    

class LoginForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(), Email()])  # use email instead of username to login 
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # yes, then browser use cookie to remember, so next time no need to enter email+pwd
    submit = SubmitField('Login')

