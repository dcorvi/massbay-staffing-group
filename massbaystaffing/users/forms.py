# massbaystaffing/users/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask import flash
from massbaystaffing.models import User

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=64, message='First name must be between 1 and 50 characters long')])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64, message='Last name must be between 1 and 50 characters long')])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64, message='Username length must be between 2 and 64 characters long')])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Not a valid email format'), Length(max=64, message='email length must be less than 64 characters')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=128, message='Passwords must be at least 3 charcters long')])
    password2 = PasswordField('Re-enter Password', validators=[DataRequired(),
    EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Register')

    # setup validation methods to be checked when form is submitted
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Use a different username/email.') # always make username and email ambigous to deter hacking

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Use a different username/email.')


class UpdateUserForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired(), Email(message='Not a valid email format'), Length(max=64, message='email length must be less than 64 characters')])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64, message='Username length must be between 2 and 64 characters long')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and user.username != username.data:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and email.data != email.data:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired(), Email(message='Not a valid email format')])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=128, message='Passwords must be at least 3 charcters long')])
    password2 = PasswordField('Re-type Password', validators=[DataRequired(), EqualTo('password',message='Passwords must match!')])
    submit = SubmitField('Reset Password')

class PostForm(FlaskForm):
    tweet = StringField('Enter blog post:', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Post')
