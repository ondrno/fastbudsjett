from typing import List
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import DecimalField, SelectField, StringField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, NumberRange
import datetime

from .auth import login_required
from . import rest
from . import utils


bp = Blueprint('items', __name__)


class ItemsForm(FlaskForm):
    date = DateField('Date', format="%Y-%m-%d", default=datetime.date.today, validators=[InputRequired()])
    payment_type = SelectField('Payment', coerce=int, validators=[InputRequired()])
    amount = DecimalField('Amount', validators=[InputRequired(), NumberRange(min=0.01)])
    category = SelectField('Category', coerce=int, validators=[InputRequired()])
    itemtype = RadioField('ItemType', coerce=int, validators=[InputRequired()])
    description = StringField('Description', validators=[
        InputRequired(),
        Length(6, 255)
    ])
    submit = SubmitField('Create')


def get_items_and_resolve(itemtypes: dict, payment_types: dict, categories: dict):
    """
    Get items using rest api and translate the payment_id, category_id
    into the names.
    """
    raw = rest.iface.get_items_for_month(2020, 12)
    # print(f"get_items_and_resolve: {raw}")
    payments = {}
    for i in raw:
        cat_id = i['category_id']
        payment_id = i['payment_id']
        itemtype_id = i['itemtype_id']

        payment = i
        payment['itemtype'] = itemtypes.get(itemtype_id)
        payment['is_revenue'] = payment['itemtype'].lower() == 'revenue'
        payment['payment'] = payment_types.get(payment_id)
        payment['category'] = categories.get(cat_id)
        year, month, day = str(payment['date']).split('-')
        if year not in payments:
            payments[year] = {}
        if month not in payments[year]:
            payments[year][month] = {}
        if day not in payments[year][month]:
            payments[year][month][day] = []
        payments[year][month][day].append(payment)

    return payments


@bp.route('/', methods=['GET'])
@login_required
def index():
    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    payments = get_items_and_resolve(itemtypes_lookup, payments_lookup, categories_lookup)

    return render_template('items/index.html', items=payments)


@bp.route('/edit/<int:item_id>', methods=['GET'])
@login_required
def edit(item_id: int):
    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    form = ItemsForm()
    form.payment_type.choices = [(k, v) for k, v in payments_lookup.items()]
    form.category.choices = [(k, v) for k, v in categories_lookup.items()]
    form.itemtype.choices = [(k, v) for k, v in itemtypes_lookup.items()]

    if form.validate_on_submit():
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        payment = request.form['payment_type']
        description = request.form['description']
        itemtype = request.form['itemtype']
        data = {'date': date, 'amount': amount, 'category_id': category,
                'payment_id': payment, 'description': description, 'itemtype_id': itemtype}
        rest.iface.create_item(data)
        return redirect(url_for('index'))

    print(f"edit {item_id}")

    return redirect(url_for('index'))


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    form = ItemsForm()
    form.payment_type.choices = [(k, v) for k, v in payments_lookup.items()]
    form.category.choices = [(k, v) for k, v in categories_lookup.items()]

    if form.validate_on_submit():
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        payment = request.form['payment_type']
        itemtype = request.form['itemtype']
        description = request.form['description']
        data = {'date': date, 'amount': amount, 'category_id': category,
                'payment_id': payment, 'description': description}
        rest.iface.create_item(data)
        return redirect(url_for('index'))

    return render_template('items/create.html', form=form)
