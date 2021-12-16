from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired(),
        Email(message='Not a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(5, 64)
    ])
    submit = SubmitField('Sign In')
