# massbaystaffing/job_posts/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField, BooleanField, DateField, RadioField, SelectField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo, Length, ValidationError, URL, Optional
from flask import flash

class JobForm(FlaskForm):
    job_title = StringField('Job Title:', validators=[InputRequired()])
    company = StringField('Company:')
    job_status = RadioField('Job Status:',choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'),('Contract', 'Contract'),('Other', 'Other')], validators=[InputRequired(message='Must select a job status')])
    job_sector = RadioField('Job Sector:',choices=[('Public', 'Public'), ('Private', 'Private'),('', '[blank]')], validators=[Optional()])
    city = StringField('City:', validators=[InputRequired()])
    state = SelectField('State:',choices=[('MA', 'MA'), ('NH', 'NH'),('VT', 'VT'),('ME', 'ME'), ('RI', 'RI')], validators=[InputRequired(message='Must select a state')])
    zip = StringField('Zip:', validators=[InputRequired(), Length(min=5,max=5, message='Zip code must be 5 characters')], render_kw={"placeholder": "00000"})
    job_description = TextAreaField('Job Description:', validators=[Length(max=500, message='Job description must be less than 500 characters')])
    job_requirements = TextAreaField('Job Requirements:', validators=[Length(max=500, message='Job requirements must be less than 500 characters')])
    job_posting_link = TextAreaField('Job Posting Link:', validators=[Optional(),Length(max=500, message='Job link must be less than 500 characters'),URL(message='Must be a URL(http://) or blank')])
    post_website = RadioField('For which website:',choices=[("1", 'Massbay Staffing'), ("2", 'Job board webite'), ("3", 'Both'), ("0", '[blank]')], validators=[Optional()])
    # job_post_date = StringField('Posting Date:', render_kw={"placeholder": "YYYY-MM-DD"})
    # submit = SubmitField()

    class SubscriberForm(FlaskForm):
        email = StringField('E-mail', validators=[DataRequired(), Email(message='Not a valid email format'), Length(max=64, message='email length must be less than 64 characters')])
