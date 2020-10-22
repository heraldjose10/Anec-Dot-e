from flask import render_template,current_app
from app.mail import send_mail


def send_password_reset_mail(user):
    token = user.get_password_request_token()
    send_mail('[Anecdote] Reset your password',sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/mail_text.txt',user=user,token=token),
        html_body=render_template('email/mail_html.html',user=user,token=token))