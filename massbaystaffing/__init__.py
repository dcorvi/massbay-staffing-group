# massbaystaffing/__init__.py
import os
from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

# setup app variables
app = Flask(__name__)

app.config.from_object(Config)


############################
### DATABASE SETUP ##########
########################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

Bootstrap(app)

#########################
# LOGIN CONFIGS
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


#########################
# EMAIl CONFIGS
mail = Mail(app)


##################################################

#########################
# BLUEPRINT CONFIG


from massbaystaffing.core.views import core
from massbaystaffing.users.views import users
from massbaystaffing.blog_posts.views import blog_posts
from massbaystaffing.job_posts.views import job_posts
from massbaystaffing.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(job_posts)
app.register_blueprint(error_pages)




##################################################
