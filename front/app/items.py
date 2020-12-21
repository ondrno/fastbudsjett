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


class ItemsCreateForm(ItemsForm):
    submit = SubmitField('Create')


class ItemsUpdateForm(ItemsForm):
    submit = SubmitField('Update')


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


@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit(item_id: int):
    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    current_item = rest.iface.get_item_by_id(item_id)
    (year, month, day) = current_item.get('date').split("-")

    form = ItemsUpdateForm(amount=current_item.get('amount'),
                           description=current_item.get('description'),
                           date=datetime.date(year=int(year), month=int(month), day=int(day))
                           )
    utils.set_form_field_default(request, form.payment_type, payments_lookup,
                                 default=payments_lookup[current_item.get('payment_id')])
    utils.set_form_field_default(request, form.category, categories_lookup,
                                 default=categories_lookup[current_item.get('category_id')])
    utils.set_form_field_default(request, form.itemtype, itemtypes_lookup,
                                 default=itemtypes_lookup[current_item.get('itemtype_id')])

    if form.validate_on_submit():
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        payment = request.form['payment_type']
        description = request.form['description']
        itemtype = request.form['itemtype']
        data = {'date': date, 'amount': amount, 'category_id': category,
                'payment_id': payment, 'description': description, 'itemtype_id': itemtype}
        rest.iface.update_item(item_id, data)
        return redirect(url_for('index'))

    return render_template('items/create.html', form=form, form_action=url_for('items.edit', item_id=item_id))


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    form = ItemsCreateForm()
    utils.set_form_field_default(request, form.payment_type, payments_lookup, 'cash')
    utils.set_form_field_default(request, form.category, categories_lookup, 'food')
    utils.set_form_field_default(request, form.itemtype, itemtypes_lookup, 'expenditure')

    if form.validate_on_submit():
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        payment = request.form['payment_type']
        itemtype = request.form['itemtype']
        description = request.form['description']
        data = {'date': date, 'amount': amount, 'category_id': category,
                'payment_id': payment, 'description': description, 'itemtype_id': itemtype}
        rest.iface.create_item(data)
        return redirect(url_for('index'))

    return render_template('items/create.html', form=form, form_action=url_for('items.create'))
