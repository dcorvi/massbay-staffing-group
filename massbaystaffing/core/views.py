# massbaystaffing/core/views.py
from flask import render_template, url_for, redirect, flash, request, Blueprint
from massbaystaffing import db
from massbaystaffing.models import Subscriber, BlogPost, ContactMessage, Job
from massbaystaffing.core.forms import ContactForm, SubscriberForm
from massbaystaffing.email import send_contact_email, newsletter_confirm_email
from flask_login import current_user, login_user, logout_user, login_required
import time

# setup blue print
core = Blueprint('core',__name__, template_folder='templates/core')

@core.route('/')
@core.route('/index')
def index():
    return render_template('index.html', title='Index')


@core.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    form = SubscriberForm()

    if form.validate_on_submit():
        # try:
        subscriber = Subscriber(
            email = form.email.data,
        )

        db.session.add(subscriber)
        db.session.commit()

        # send email
        newsletter_confirm_email(subscriber)
        flash(f'Thanks for joining the Massbay Staffing Newsletter! A confirmation email has been sent to {form.email.data}', "info")
        return redirect(url_for('core.newsletter'))

    elif not form.validate_on_submit() and request.method != 'GET':
        flash("It looks like this email is already signed up. Please choose another", "warning")
        return redirect(url_for('core.newsletter'))

    return render_template('newsletter.html', form=form, title='Newsletter')

@core.route('/positions')
def positions():
    page = request.args.get('page', 1, type=int)
    job_posts = Job.query.order_by(Job.id.desc()).paginate(page=page, per_page=5)
    return render_template('positions.html',job_posts=job_posts, title='Available Positions')


@core.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', title='About Us')

@core.route('/blog')
def blog():

    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html',blog_posts=blog_posts, title='Blog')


@core.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            contact = ContactMessage(
                name = form.name.data,
                email = form.email.data,
                phone = form.phone.data,
                message = form.message.data
            )

            db.session.add(contact)
            db.session.commit()

            # send email
            send_contact_email(contact)
            flash(f'Thanks for your submission, we will contact you shortly. A copy has been sent to {form.email.data}', "info")
            return redirect(url_for('core.index'))
        except:
            flash('Sorry your submission did not go through. Try again.', 'error')
            return redirect(url_for('core.contact'))

    return render_template('contactus.html', form=form, title='Contact')


@core.route('/contact-<int:message_id>/contact_resend', methods=['GET'])
def contact_resend(message_id):
    try:
        contact = ContactMessage.query.get_or_404(message_id)
        # send email
        send_contact_email(contact)
        flash(f'Message resent from strong{contact.email} to {current_user.email}', "info")
        return redirect(url_for('users.account'))
    except:
        flash('Message could not be resent. Try again.', 'error')
        return redirect(url_for('users.account'))


# Contact Message (DELETE)
@core.route("/contact-<int:message_id>/delete", methods=['POST'])
@login_required
def delete_contact_mess(message_id):
    contact_mess = ContactMessage.query.get_or_404(message_id)
    # if current_user != admin:
    #     abort(403)
    db.session.delete(contact_mess)
    db.session.commit()
    flash('Contact message deleted', "info")
    return redirect(url_for('users.account'))

# Subscriber (DELETE)
@core.route("/subscriber-<int:subscriber_id>/delete", methods=['POST'])
@login_required
def delete_subscriber(subscriber_id):
    subscriber = Subscriber.query.get_or_404(subscriber_id)
    # if current_user != admin:
    #     abort(403)
    db.session.delete(subscriber)
    db.session.commit()
    flash('Subscriber deleted', "info")
    return redirect(url_for('users.account'))
