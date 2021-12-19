from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import Optional
from .. import utils


class SearchForm(FlaskForm):
    start_date = DateField('From', validators=[Optional()], default=utils.start_of_year, format="%Y-%m-%d")
    end_date = DateField('Until', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    submit = SubmitField(lazy_gettext('Search'))
