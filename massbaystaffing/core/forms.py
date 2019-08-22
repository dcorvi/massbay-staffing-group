# massbaystaffing/core/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, Length, ValidationError
from flask import flash
from massbaystaffing.models import Subscriber


class ContactForm(FlaskForm):
    name = StringField('Full Name:')
    email = StringField('E-mail:', validators=[DataRequired(), Email(message='Not a valid email format'), Length(max=64, message='email length must be less than 64 characters')])
    phone = StringField('Phone:', validators=[Length(max=10, message='Phone number must be less than 10 characters')])
    message = TextAreaField('Message:', validators=[DataRequired(), Length(max=500, message='Message length must be less than 500 characters')])
    submit = SubmitField('Contact')



class SubscriberForm(FlaskForm):
    email = StringField('E-mail',id='recipient-name', validators=[InputRequired(message='Provide an email'), Email(message='Not a valid email format'), Length(max=64, message='email length must be less than 64 characters')])
    submit = SubmitField('Subscribe')

    def validate_email(self, email):
        subscriber = Subscriber.query.filter_by(email=email.data).first()
        if subscriber is not None:
            raise ValidationError('It looks like this email is already signed up. Please choose another')
