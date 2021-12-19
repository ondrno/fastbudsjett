from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_babel import lazy_gettext


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired(),
        Email(message=lazy_gettext('Not a valid email address.'))
    ])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(5, 64)
    ])
    submit = SubmitField(lazy_gettext('Sign In'))
