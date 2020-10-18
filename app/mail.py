from flask_mail import Message
from flask import render_template
from app import mail,app


def send_mail(subject,sender,recipients,text_body,html_body):
    msg = Message(subject,sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_mail(user):
    token = user.get_password_request_token()
    send_mail('[Anecdote] Reset your password',sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/mail_text.txt',user=user,token=token),
        html_body=render_template('email/mail_html.html',user=user,token=token))
