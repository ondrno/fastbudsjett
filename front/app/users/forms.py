from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired


class UsersForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    default_locale = SelectField('Language', choices=[('en', 'English'), ('de', 'Deutsch')],
                                 validators=[InputRequired()])
    submit = SubmitField('Update')
