from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_babel import lazy_gettext


class CategoriesForm(FlaskForm):
    title_en = StringField(lazy_gettext('Title (English)'), validators=[
        InputRequired(),
        Length(5, 30)
    ])
    title_de = StringField(lazy_gettext('Title (German)'), validators=[
        InputRequired(),
        Length(5, 30)
    ])
    itemtype = SelectField(lazy_gettext('Expense Type'), coerce=int, validators=[InputRequired()])
    submit = SubmitField('Create')
