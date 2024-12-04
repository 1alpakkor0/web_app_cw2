from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class ChangePasswordForm(FlaskForm): ## This is the change password form 
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')



class LoginForm(FlaskForm): ## This is the login form
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class SignupForm(FlaskForm): ## This is the signup form
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email): ## This is for checking if the email already exists in the database or not 
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already exists.')    
        

class DeleteAccountForm(FlaskForm): ## This is the delete account form
    # email = StringField('Email', validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # submit = SubmitField('Delete Account')
    pass