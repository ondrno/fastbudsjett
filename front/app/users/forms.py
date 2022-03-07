from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired


class UsersForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    default_locale = SelectField('Language', choices=[('en', 'English'), ('de', 'Deutsch')],
                                 validators=[InputRequired()])
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)
    submit = SubmitField('Update')
