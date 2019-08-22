# massbaystaffing/email.py
from flask_mail import Message
from flask import render_template
from massbaystaffing import mail, app

from threading import Thread

# Send emails asynchronously for speed
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg)
    # Send emails asynchronously for speed
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        subject = 'Massbay Staffing - Password Reset',
        sender = ('Massbay Staffing Group', app.config['ADMINS'][0]),
        recipients = [user.email],
        text_body = render_template('email/reset_password.txt', user=user, token=token),
        html_body = render_template('email/reset_password.html',
        user=user, token=token)
    )

def newsletter_confirm_email(subscriber):
    send_email(
        'The Massbay Staffing Group Newsletter',
        sender = ('Massbay Staffing Group', app.config['ADMINS'][0]),
        recipients = [subscriber.email],
        text_body = render_template('email/newsletter_confirm_email.txt', subscriber=subscriber),
        html_body = render_template('email/newsletter_confirm_email.html', subscriber=subscriber)
    )


def send_email2(subject, sender, recipients, cc, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients, cc=cc)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg)
    # Send emails asynchronously for speed
    Thread(target=send_async_email, args=(app, msg)).start()


def send_contact_email(contact):
    send_email2(
        'Contact',
        sender = ('Massbay Staffing Group', app.config['ADMINS'][0]),
        recipients = [app.config['ADMINS'][0]],
        cc = [contact.email],
        text_body = render_template('email/contact_email.txt', contact=contact),
        html_body = render_template('email/contact_email.html', contact=contact)
    )
