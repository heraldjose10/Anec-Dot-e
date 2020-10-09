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

class EditProfileForm(FlaskForm):
        username = StringField('Username',validators=[DataRequired()])
        about_me = TextAreaField('About Me',validators=[Length(min=0,max=140)])
        submit = SubmitField('Submit')
    
        def __init__(self, original_username ,*args, **kwargs):
            super(EditProfileForm,self).__init__(*args, **kwargs)
            self.original_username= original_username

        def validate_username(self,username):
            if username.data!=self.original_username:
                user = User.query.filter_by(username=self.username.data).first()
                if user is not None:
                    raise ValidationError('This Username is Taken')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Whats on Your Mind NOW?',validators=[DataRequired(),Length(min=1,max=140)])
    submit = SubmitField('Submit')