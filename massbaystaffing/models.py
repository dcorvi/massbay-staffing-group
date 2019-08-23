#massbaystaffing/models.py
from massbaystaffing import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from time import time
import jwt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime,nullable=False,default=datetime.now())

    posts = db.relationship('BlogPost',backref='author',lazy=True)
    jobs = db.relationship('Job',backref='jobposter',lazy=True)


    def __init__(self,first_name,last_name,email,username,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

## new code
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            { 'reset_password': self.id, 'exp': time() + expires_in },
            app.config['SECRET_KEY'], algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithm=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f"Username {self.username}"


class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.now())
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"

class ContactMessage(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(10))
    message = db.Column(db.Text)
    date = db.Column(db.DateTime,nullable=False,default=datetime.now())

    def __init__(self,name,email,phone,message):
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message

    def __repr__(self):
        return f"ContactEmail ID: {self.id} -- Date: {self.date} -- Name: {self.name} -- Email: {self.email} -- Phone: {self.phone}"


class Job(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    job_title = db.Column(db.String(500),nullable=False, index=True)
    company = db.Column(db.String(500))
    city = db.Column(db.String(500))
    state = db.Column(db.String(2), nullable=False, index=True)
    zip = db.Column(db.String(5))
    job_description = db.Column(db.Text)
    job_requirements = db.Column(db.Text)
    job_status = db.Column(db.String(100))
    job_sector = db.Column(db.String(500))
    job_type = db.Column(db.String(500))
    post_website = db.Column(db.Integer)
    job_posting_link = db.Column(db.String(500))
    # job_post_date = db.Column(db.DateTime, default=None)
    # job_post_date = db.Column(db.DateTime, default=datetime.now().date())
    job_creation_date = db.Column(db.DateTime,nullable=False,default=datetime.now())

    def __init__(self,job_title,company,city,state,zip,job_description,job_requirements,job_status,job_sector,job_type,post_website,job_posting_link,user_id):
        self.job_title = job_title
        self.company = company
        self.city = city
        self.state = state
        self.zip = zip
        self.job_description = job_description
        self.job_requirements = job_requirements
        self.job_status = job_status
        self.job_sector = job_sector
        self.job_type = job_type
        self.post_website = post_website
        self.job_posting_link = job_posting_link
        self.user_id = user_id

    def __repr__(self):
        return f"Job ID: {self.id} -- title: {self.job_title} -- company: {self.company}"

class Subscriber(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64), index=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.now())

    def __init__(self,email):
        self.email = email

    def __repr__(self):
        return f"Subscriber ID: {self.id} -- Email: {self.email}"
