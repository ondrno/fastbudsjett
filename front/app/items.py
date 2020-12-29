from typing import List
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, g
)
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import DecimalField, SelectField, StringField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, NumberRange
import datetime
import calendar
from dateutil.relativedelta import relativedelta

from .auth import login_required
from . import rest
from . import utils
from . import search


bp = Blueprint('items', __name__)


class ItemsForm(FlaskForm):
    date = DateField('Date', format="%Y-%m-%d", default=datetime.date.today, validators=[InputRequired()])
    payment_type = SelectField('Payment', coerce=int, validators=[InputRequired()])
    amount = DecimalField('Amount', places=2, validators=[InputRequired(), NumberRange(min=0.01)])
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


def resolve_items(raw, itemtypes: dict, payment_types: dict, categories: dict):
    payments = {}
    payments['sum_expenditures'] = 0
    payments['sum_revenues'] = 0
    for i in raw:
        cat_id = i['category_id']
        payment_id = i['payment_id']
        itemtype_id = i['itemtype_id']

        payment = i
        payment['itemtype'] = itemtypes.get(itemtype_id)
        payment['is_revenue'] = payment['itemtype'].lower() == 'revenue'
        payment['payment'] = payment_types.get(payment_id)
        payment['category'] = categories.get(cat_id)
        year, month, day = [int(i) for i in str(payment['date']).split('-')]
        if year not in payments:
            payments[year] = {}
            payments[year]['sum_revenues'] = 0
            payments[year]['sum_expenditures'] = 0
        if month not in payments[year]:
            payments[year][month] = {}
            payments[year][month]['sum_revenues'] = 0
            payments[year][month]['sum_expenditures'] = 0
        if day not in payments[year][month]:
            payments[year][month][day] = {}
            now = datetime.date(year, month, day)
            payments[year][month][day]['weekday'] = calendar.day_abbr[now.weekday()]
            payments[year][month][day]['entries'] = []
            payments[year][month][day]['sum_expenditures'] = 0
            payments[year][month][day]['sum_revenues'] = 0
        payments[year][month][day]['entries'].append(payment)
        if payment['is_revenue']:
            payments[year][month][day]['sum_revenues'] += payment['amount']
            payments[year][month]['sum_revenues'] += payment['amount']
            payments[year]['sum_revenues'] += payment['amount']
            payments['sum_revenues'] += payment['amount']
        else:
            payments[year][month][day]['sum_expenditures'] += payment['amount']
            payments[year][month]['sum_expenditures'] += payment['amount']
            payments[year]['sum_expenditures'] += payment['amount']
            payments['sum_expenditures'] += payment['amount']

    return payments


def get_items_and_resolve(itemtypes: dict, payment_types: dict, categories: dict):
    """
    Get items using rest api and translate the payment_id, category_id
    into the names.
    """
    today = datetime.datetime.today()
    if 'curr_month' not in g:
        g.curr_month = f"{today.year}/{today.month}"

    year, month = [int(i) for i in g.curr_month.split("/")]
    raw = rest.iface.get_items_for_month(year, month)
    return resolve_items(raw, itemtypes, payment_types, categories)


@bp.route('/', methods=['GET'])
@login_required
def index():
    today = datetime.datetime.today()
    return redirect(url_for('items.show', year=today.year, month=today.month))


def calc_next_and_prev_month(now: datetime.date):
    next_month = now + relativedelta(months=+1)
    prev_month = now + relativedelta(months=-1)

    g.curr_month = f"{now.year}/{now.month}"
    g.curr_month_abbr = calendar.month_abbr[now.month]

    g.prev_month = f"{prev_month.year}/{prev_month.month}"
    g.next_month = f"{next_month.year}/{next_month.month}"


@bp.route('/show/<int:year>/<int:month>', methods=['GET'])
@login_required
def show(year: int, month: int):
    now = datetime.date(year, month, 1)

    search_form = search.SearchForm()
    calc_next_and_prev_month(now)

    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    payments = get_items_and_resolve(itemtypes_lookup, payments_lookup, categories_lookup)

    return render_template('items/index.html', items=payments, search_form=search_form)


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

    return render_template('items/create_or_edit.html', form=form, form_action=url_for('items.edit', item_id=item_id))


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

    return render_template('items/create_or_edit.html', form=form, form_action=url_for('items.create'))
