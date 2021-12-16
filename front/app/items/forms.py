from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, NumberRange
import datetime


class ItemsForm(FlaskForm):
    date = DateField('Date', format="%Y-%m-%d", default=datetime.date.today, validators=[InputRequired()])
    payment_type = SelectField('Payment', coerce=int, validators=[InputRequired()])
    amount = DecimalField('Amount', places=2, validators=[InputRequired(), NumberRange(min=0.01)])
    category = SelectField('Category', coerce=int, validators=[InputRequired()])
    itemtype = SelectField('ItemType', coerce=int, validators=[InputRequired()])
    description = StringField('Description', validators=[
        InputRequired(),
        Length(5, 255)
    ])
    submit = SubmitField('Create')
