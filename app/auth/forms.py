from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Your Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep Me Signed In')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email-ID',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign In')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username Exists')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This E-mail ID is already registered')


class ResetPasswordRequestForm(FlaskForm):
    email = TextAreaField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request password request')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Enter New Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat New Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')