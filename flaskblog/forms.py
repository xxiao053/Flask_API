from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import sql_validate_username, sql_validate_email
from flaskblog import engine
from sqlalchemy import text

class RegistrationForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 
    # design the form and validation  
    # create a string field for username, cannot be empty, and length between 2 and 20 char
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        with engine.connect() as conn:
            user = conn.execute(text(sql_validate_username), {"username": username.data}).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        with engine.connect() as conn:
            user = conn.execute(text(sql_validate_email), {"email": email.data}).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(), Email()])  # use email instead of username to login 
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # yes, then browser use cookie to remember, so next time no need to enter email+pwd
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:  # only if user enter a different username from their current name
            with engine.connect() as conn:
                user = conn.execute(text(sql_validate_username), {"username": username.data}).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            with engine.connect() as conn:
                user = conn.execute(text(sql_validate_email), {"email": email.data}).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')