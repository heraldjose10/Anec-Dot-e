from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField('Your Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember_me=BooleanField('Keep Me Signed In')
    submit=SubmitField('Log In')