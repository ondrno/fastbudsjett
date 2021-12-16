from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length


class CategoriesForm(FlaskForm):
    name = StringField('Description', validators=[
        InputRequired(),
        Length(5, 30)
    ])
    itemtype = SelectField('ItemType', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Create')
