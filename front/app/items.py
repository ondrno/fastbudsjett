from typing import List
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length


from .auth import login_required
from . import rest
from . import categories
from . import payment_types

bp = Blueprint('items', __name__)


class ItemsForm(FlaskForm):
    date = DateField('Date', validators=[InputRequired()])
    payment_type = SelectField('Payment', coerce=int, validators=[InputRequired()])
    amount = DecimalField('Amount', validators=[InputRequired()])
    category = SelectField('Category', coerce=int, validators=[InputRequired()])
    description = StringField('Description', validators=[
        InputRequired(),
        Length(5, 255)
    ])
    submit = SubmitField('Create')


def get_items_and_resolve(payment_types, categories):
    """
    Get items using rest api and translate the payment_id, category_id
    into the names.
    """
    raw = rest.iface.get_items()
    print(f"get_items_and_resolve: {raw}")
    payments = []
    for i in raw:
        cat_id = i['category_id']
        payment_id = i['payment_id']

        payment = i
        payment['payment'] = payment_types.get(payment_id)
        payment['category'] = categories.get(cat_id)
        payments.append(payment)

    return payments

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    categories_lookup = categories.get_categories()
    payments_lookup = payment_types.get_payments()

    form = ItemsForm()
    form.payment_type.choices = [(k, v) for k, v in payments_lookup.items()]
    form.category.choices = [(k, v) for k, v in categories_lookup.items()]

    payments = get_items_and_resolve(payments_lookup, categories_lookup)

    # if request.method == 'POST':
    #     date = request.form['inputDate']
    #     amount = request.form['inputAmount']
    #     category = request.form['inputCategory']
    #     payment = request.form['inputPayment']
    #     description = request.form['inputDescription']
    #     # TODO
    # print(categories_sorted.items())
    # print(payments_sorted.items())

    return render_template('items/index.html', items=payments, form=form)
