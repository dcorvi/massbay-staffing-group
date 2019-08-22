# massbaystaffing/core/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask import flash


class ContactForm(FlaskForm):
    name = StringField('Full Name:')
    email = StringField('E-mail:', validators=[DataRequired(), Email(message='Not a valid email format'), Length(max=64, message='email length must be less than 64 characters')])
    phone = StringField('Phone:', validators=[Length(max=10, message='Phone number must be less than 10 characters')])
    message = TextAreaField('Message:', validators=[DataRequired(), Length(max=500, message='Message length must be less than 500 characters')])
    submit = SubmitField('Contact')



# class PostForm(FlaskForm):
#     tweet = StringField('Enter blog post:', validators=[DataRequired(), length(max=500)])
#     submit = SubmitField('Post')
