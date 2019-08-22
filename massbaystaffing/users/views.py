# massbaystaffing/users/views.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from massbaystaffing import db
from massbaystaffing.users.forms import LoginForm, RegisterForm, UpdateUserForm, ResetPasswordRequestForm, ResetPasswordForm, PostForm
from massbaystaffing.models import User, BlogPost, Job
from massbaystaffing.email import send_password_reset_email
import time

users = Blueprint('users',__name__, template_folder='templates/users')


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    username = form.username.data,
                    email = form.email.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()

        # need to add email confirmation
        flash(f'Thanks for registering!', "success")
        return redirect(url_for('users.login'))

    return render_template('form.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    # if user is already logged in, send them to the profile page
    # if current_user.is_authenticated:
    #     flash('You are already logged in!')
    #     return redirect(url_for('users.account',username=current_user.username))

    if form.validate_on_submit():
        # query the database for the user trying to log in
        user = User.query.filter_by(email=form.email.data).first()

        # if user doesn't exist, reload the page and flash message
        # or if the password doesn't match the password stored
        if user is None or not user.check_password(form.password.data):
            flash('Credentials are incorrect.', "error")
            return redirect(url_for('users.login'))

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Logged in', "info")

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('users.account')

            return redirect(next)

    return render_template('form.html', title='Login', form=form)

@login_required
@users.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username=''):
    form = PostForm()

    # posts = Post.query.all()

    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        post = Post(tweet=form.tweet.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('users.profile', username=username))

    return render_template('profile.html', title='Profile', form=form, user=user)

@users.route('/logout')
def logout():
    logout_user()
    # flash('You have been logged out!')
    return redirect(url_for('users.login'))


# account (update UserForm)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    # job_posts = Job.query.all()
    form1 = UpdateUserForm()
    user = current_user.username
    page = request.args.get('page', 1, type=int)
    # blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    job_posts = Job.query.order_by(Job.id.asc()).paginate(page=page, per_page=5)


    if form1.validate_on_submit():
        current_user.username = form1.username.data
        current_user.email = form1.email.data
        db.session.commit()
        flash('User Account Updated', "info")
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form1.username.data = current_user.username
        form1.email.data = current_user.email

    return render_template('account.html', form1=form1, title="Account", job_posts=job_posts)

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)



######################  Password Resetting ##############################
### have to setup app password in config file and google account ###
@users.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        flash("You are currently logged in, please sign out", "info")
        return redirect(url_for('core.index'))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password.', "info")
        return redirect(url_for('users.login'))

    return render_template('reset_password_request.html', title="Reset Password", form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash("You are currently logged in, please sign out", "info")
        return redirect(url_for('core.index'))

    user = User.verify_reset_password_token(token)

    if not user:
        flash("Error", "error")
        return redirect(url_for('core.index'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', "info")
        return redirect(url_for('users.login'))

    return render_template('reset_password_request.html', form=form)
