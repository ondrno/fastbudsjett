from flask import (
    Blueprint, g, redirect, render_template, request, url_for, session
)
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, NumberRange
import datetime
import calendar
from dateutil.relativedelta import relativedelta
import json
import jsonpickle

from .auth import login_required
from . import rest
from front.app.utils import utils


bp = Blueprint('items', __name__)


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


def resolve_items(raw,
                  itemtypes: utils.ItemTypes,
                  payment_types: utils.PaymentTypes,
                  categories: utils.CategoryTypes):
    payments = {}
    payments['sum_expenses'] = 0
    payments['sum_income'] = 0
    for i in raw:

        cat_id = i['category_id']
        payment_id = i['payment_id']
        itemtype_id = i['itemtype_id']

        payment = i
        payment['itemtype'] = itemtypes.get_value(itemtype_id)
        payment['is_income'] = payment['itemtype'].lower() == 'revenue'
        payment['payment'] = payment_types.get_value(payment_id)
        payment['category'] = categories.get_value(cat_id)
        year, month, day = [int(i) for i in str(payment['date']).split('-')]
        if year not in payments:
            payments[year] = {}
            payments[year]['sum_income'] = 0
            payments[year]['sum_expenses'] = 0
        if month not in payments[year]:
            payments[year][month] = {}
            payments[year][month]['sum_income'] = 0
            payments[year][month]['sum_expenses'] = 0
        if day not in payments[year][month]:
            payments[year][month][day] = {}
            now = datetime.date(year, month, day)
            payments[year][month][day]['weekday'] = calendar.day_abbr[now.weekday()]
            payments[year][month][day]['entries'] = []
            payments[year][month][day]['sum_expenses'] = 0
            payments[year][month][day]['sum_income'] = 0
        payments[year][month][day]['entries'].append(payment)
        if payment['is_income']:
            payments[year][month][day]['sum_income'] += payment['amount']
            payments[year][month]['sum_income'] += payment['amount']
            payments[year]['sum_income'] += payment['amount']
            payments['sum_income'] += payment['amount']
        else:
            payments[year][month][day]['sum_expenses'] += payment['amount']
            payments[year][month]['sum_expenses'] += payment['amount']
            payments[year]['sum_expenses'] += payment['amount']
            payments['sum_expenses'] += payment['amount']

    return payments


def get_items_and_resolve(itemtypes: utils.ItemTypes,
                          payment_types: utils.PaymentTypes,
                          categories: utils.CategoryTypes):
    """
    Get items using rest api and translate the payment_id, category_id
    into the names.
    """
    year, month = get_year_month_from_url()
    if 'curr_month' not in g:
        g.curr_month = format_suburl(year, month)

    raw = rest.iface.get_items_for_month(year, month)
    return resolve_items(raw, itemtypes, payment_types, categories)


def calc_next_and_prev_month(now: datetime.date):
    next_month = now + relativedelta(months=+1)
    prev_month = now + relativedelta(months=-1)

    g.curr_month = format_suburl(now.year, now.month)
    session["selected_month"] = g.curr_month
    g.curr_month_abbr = calendar.month_abbr[now.month]

    g.prev_month = format_suburl(prev_month.year, prev_month.month)
    g.next_month = format_suburl(next_month.year, next_month.month)


def get_year_month_from_url(sub_url: str = None) -> (int, int):
    """
        Extract the year and month from a string in the format 'year/month'
        If sub_url is not provided the session variable selected_month is
        used as default
    """
    if not sub_url:
        if 'selected_month' in session:
            sub_url = session["selected_month"]
        else:
            today = datetime.datetime.today()
            year = today.year
            month = today.month
            sub_url = format_suburl(year, month)
    year, month = [int(i) for i in sub_url.split("/")]
    return year, month


def format_suburl(year: int, month: int) -> str:
    return f"{year}/{month}"


def prepare_data(r: request):
    data = {'date': r.form['date'],
            'amount': r.form['amount'],
            'category_id': r.form['category'],
            'payment_id': r.form['payment_type'],
            'description': r.form['description'],
            'itemtype_id': r.form['itemtype']
            }
    return data


def types_to_session(categories, payments, itemtypes):
    session["categories"] = jsonpickle.encode(categories)
    session["payments"] = jsonpickle.encode(payments)
    session["itemtypes"] = jsonpickle.encode(itemtypes)


def types_from_session() -> dict:
    return {
        'categories': jsonpickle.decode(session["categories"]),
        'payments': jsonpickle.decode(session["payments"]),
        'itemtypes': jsonpickle.decode(session["itemtypes"]),
    }


def is_form_only(r: request):
    return 'form_only' in request.args and request.method == 'GET'


@bp.route('/', methods=['GET'])
@login_required
def index():
    year, month = get_year_month_from_url()
    return redirect(url_for('items.show', year=year, month=month))


@bp.route('/show/<int:year>/<int:month>', methods=['GET'])
@login_required
def show(year: int, month: int):
    now = datetime.date(year, month, 1)
    calc_next_and_prev_month(now)

    categories = utils.CategoryTypes()
    payments = utils.PaymentTypes()
    itemtypes = utils.ItemTypes()
    types_to_session(categories, payments, itemtypes)

    form = ItemsForm()
    utils.set_form_field_default(request, form.payment_type, payments, 'cash')
    utils.set_form_field_default(request, form.category, categories, 'food')
    utils.set_form_field_default(request, form.itemtype, itemtypes, 'expenditure')

    payments = get_items_and_resolve(itemtypes, payments, categories)

    other = rest.iface.get_categories()
    print(f"categories json: {other}")

    return render_template('items/index.html', items=payments, form=form)


@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit(item_id: int):
    form_only = is_form_only(request)
    t = types_from_session()
    categories = t["categories"]
    payments = t["payments"]
    itemtypes = t["itemtypes"]

    current_item = rest.iface.get_item_by_id(item_id)
    (year, month, day) = current_item.get('date').split("-")

    form = ItemsForm(amount=current_item.get('amount'),
                     description=current_item.get('description'),
                     date=datetime.date(year=int(year), month=int(month), day=int(day))
                     )
    utils.set_form_field_default(request, form.payment_type, payments,
                                 default=payments.get_value(current_item.get('payment_id')))
    utils.set_form_field_default(request, form.category, categories,
                                 default=categories.get_value(current_item.get('category_id')))
    utils.set_form_field_default(request, form.itemtype, itemtypes,
                                 default=itemtypes.get_value(current_item.get('itemtype_id')))

    if form.validate_on_submit():
        data = prepare_data(request)
        rest.iface.update_item(item_id, data)

        # show the same month as the date of the item which was created/modified
        session["selected_month"] = "/".join(data['date'].split("-")[0:2])
        return redirect(url_for('index'))

    if form_only:
        html_form = render_template('items/item_edit_form.html', form=form, form_action=url_for('items.edit', item_id=item_id))
        return json.dumps({'html_form': html_form})

    return render_template('items/create_or_edit.html', form=form, form_action=url_for('items.edit', item_id=item_id))


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form_only = is_form_only(request)
    t = types_from_session()

    form = ItemsForm()
    utils.set_form_field_default(request, form.payment_type, t['payments'], 'cash')
    utils.set_form_field_default(request, form.category, t['categories'], 'food')
    utils.set_form_field_default(request, form.itemtype, t['itemtypes'], 'expenditure')

    if form.validate_on_submit():
        data = prepare_data(request)
        rest.iface.create_item(data)

        # show the same month as the date of the item which was created/modified
        session["selected_month"] = "/".join(data['date'].split("-")[0:2])
        return redirect(url_for('index'))

    if form_only:
        html_form = render_template('items/item_edit_form.html', form=form, form_action=url_for('items.create'))
        return json.dumps({'html_form': html_form})

    return render_template('items/create_or_edit.html', form=form, form_action=url_for('items.create'))


@bp.route('/remove/<int:item_id>', methods=['GET', 'POST'])
@login_required
def remove(item_id: int):
    form_only = is_form_only(request)
    categories = jsonpickle.decode(session["categories"])
    payments = jsonpickle.decode(session["payments"])
    itemtypes = jsonpickle.decode(session["itemtypes"])

    current_item = rest.iface.get_item_by_id(item_id)
    (year, month, day) = current_item.get('date').split("-")

    form = ItemsForm(amount=current_item.get('amount'),
                     description=current_item.get('description'),
                     date=datetime.date(year=int(year), month=int(month), day=int(day))
                     )

    utils.set_form_field_default(request, form.payment_type, payments,
                                 default=payments.get_value(current_item.get('payment_id')))
    utils.set_form_field_default(request, form.category, categories,
                                 default=categories.get_value(current_item.get('category_id')))
    utils.set_form_field_default(request, form.itemtype, itemtypes,
                                 default=itemtypes.get_value(current_item.get('itemtype_id')))
    for k in form.__dict__['_fields'].keys():
        if k == "submit" or k == "crsf_token":
            continue
        form.__dict__['_fields'][k].render_kw = {'readonly': 'readonly'}

    if form.validate_on_submit():
        data = prepare_data(request)
        rest.iface.purge_item(item_id, data)

        return redirect(url_for('index'))

    if form_only:
        html_form = render_template('items/item_remove_form.html',
                                    form=form, form_action=url_for('items.remove', item_id=item_id))
        return json.dumps({'html_form': html_form})

    return render_template('items/remove.html', form=form, form_action=url_for('items.remove', item_id=item_id))
