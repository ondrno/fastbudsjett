from flask import (
    Blueprint, g, redirect, render_template, request, url_for, session
)
import datetime
from dateutil.relativedelta import relativedelta
import json
import jsonpickle

from ..auth.controllers import login_required
from ..utils import utils, rest
from .forms import ItemsForm


mod_items = Blueprint('items', __name__, url_prefix="/items")


def resolve_items(raw,
                  itemtypes: utils.ItemTypes,
                  payment_types: utils.PaymentTypes,
                  income_categories: utils.CategoryTypes,
                  expense_categories: utils.CategoryTypes):
    payments = {}
    payments['sum_expenses'] = 0
    payments['sum_income'] = 0
    for i in raw:

        cat_id = i['category_id']
        payment_id = i['payment_id']
        itemtype_id = i['itemtype_id']

        payment = i
        payment['itemtype'] = itemtypes.get_title_for_id(itemtype_id)

        # this is hard-coded stuff depending on title of the itemtype
        # better have a field in db indicating that this itemtype id is the income
        itemtype_title_en = itemtypes.get_title_for_id(itemtype_id, 'en')
        is_income = itemtype_title_en.lower() == 'income'
        payment['is_income'] = is_income
        if is_income:
            categories = income_categories
        else:
            categories = expense_categories

        payment['payment'] = payment_types.get_title_for_id(payment_id)
        payment['category'] = categories.get_title_for_id(cat_id)
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
            payments[year][month][day]['weekday'] = now.weekday()
            payments[year][month][day]['weekday_abbr'] = utils.day_name(now.weekday())
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
                          income_categories: utils.CategoryTypes,
                          expense_categories: utils.CategoryTypes):
    """
    Get items using rest api and translate the payment_id, category_id
    into the names.
    """
    year, month = get_year_month_from_url()
    if 'curr_month' not in g:
        g.curr_month = format_suburl(year, month)

    raw = rest.iface.get_items_for_month(year, month)
    return resolve_items(raw, itemtypes, payment_types, income_categories, expense_categories)


def calc_next_and_prev_month(now: datetime.date):
    next_month = now + relativedelta(months=+1)
    prev_month = now + relativedelta(months=-1)

    g.curr_month = format_suburl(now.year, now.month)
    session["selected_month"] = g.curr_month

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


def is_form_only(r: request):
    return 'form_only' in request.args and request.method == 'GET'


@mod_items.route('/', methods=['GET'])
@login_required
def index():
    year, month = get_year_month_from_url()
    return redirect(url_for('items.show', year=year, month=month))


@mod_items.route('/show/<int:year>/<int:month>', methods=['GET'])
@login_required
def show(year: int, month: int):
    now = datetime.date(year, month, 1)
    calc_next_and_prev_month(now)

    itemtypes = utils.ItemTypes()
    data = {}
    data['itemtype_id'] = itemtypes.get_id_for_income()
    income_categories = utils.CategoryTypes(data=data)
    print(f"items/controller income_categories={income_categories.entries}")

    data['itemtype_id'] = itemtypes.get_id_for_expense()
    expense_categories = utils.CategoryTypes(data=data)
    print(f"items/controller expense_categories={expense_categories.entries}")
    payments = utils.PaymentTypes()

    utils.types_to_session(income_categories, expense_categories, payments, itemtypes)

    form = ItemsForm()
    utils.set_form_field_default(request, form.payment_type, payments, 'cash')
    utils.set_form_field_default(request, form.category, expense_categories, 'food')
    utils.set_form_field_default(request, form.itemtype, itemtypes, 'expenditure')

    payments = get_items_and_resolve(itemtypes, payments, income_categories, expense_categories)

    return render_template('items/index.html', items=payments, form=form)



@mod_items.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit(item_id: int):
    form_only = is_form_only(request)
    t = utils.types_from_session()
    income_categories = t["income_categories"]
    expense_categories = t["expense_categories"]
    payments = t["payments"]
    itemtypes = t["itemtypes"]

    current_item = rest.iface.get_item_by_id(item_id)
    (year, month, day) = current_item.get('date').split("-")

    form = ItemsForm(amount=current_item.get('amount'),
                     description=current_item.get('description'),
                     date=datetime.date(year=int(year), month=int(month), day=int(day))
                     )
    utils.set_form_field_default(request, form.payment_type, payments,
                                 default=payments.get_id_for_title(current_item.get('payment_id')))
    utils.set_form_field_default(request, form.category, categories,
                                 default=categories.get_id_for_title(current_item.get('category_id')))
    utils.set_form_field_default(request, form.itemtype, itemtypes,
                                 default=itemtypes.get_id_for_title(current_item.get('itemtype_id')))

    if form.validate_on_submit():
        data = utils.prepare_data(request)
        rest.iface.update_item(item_id, data)

        # show the same month as the date of the item which was created/modified
        session["selected_month"] = "/".join(data['date'].split("-")[0:2])
        return redirect(url_for('items.index'))

    if form_only:
        html_form = render_template('items/item_edit_form.html', form=form, form_action=url_for('items.edit', item_id=item_id))
        return json.dumps({'html_form': html_form})

    return render_template('items/create_or_edit.html', form=form, form_action=url_for('items.edit', item_id=item_id))


@mod_items.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form_only = is_form_only(request)
    t = utils.types_from_session()

    form = ItemsForm()
    utils.set_form_field_default(request, form.payment_type, t['payments'], 'cash')
    utils.set_form_field_default(request, form.category, t['expense_categories'], 'food')
    utils.set_form_field_default(request, form.itemtype, t['itemtypes'], 'Ausgabe')

    if form.validate_on_submit():
        data = utils.prepare_data(request)
        rest.iface.create_item(data)

        # show the same month as the date of the item which was created/modified
        session["selected_month"] = "/".join(data['date'].split("-")[0:2])
        return redirect(url_for('items.index'))

    if form_only:
        html_form = render_template('items/item_edit_form.html', form=form, form_action=url_for('items.create'))
        return json.dumps({'html_form': html_form})

    return render_template('items/create_or_edit.html', form=form, form_action=url_for('items.create'))


@mod_items.route('/remove/<int:item_id>', methods=['GET', 'POST'])
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
                                 default=payments.get_id_for_title(current_item.get('payment_id')))
    utils.set_form_field_default(request, form.category, categories,
                                 default=categories.get_id_for_title(current_item.get('category_id')))
    utils.set_form_field_default(request, form.itemtype, itemtypes,
                                 default=itemtypes.get_id_for_title(current_item.get('itemtype_id')))
    for k in form.__dict__['_fields'].keys():
        if k == "submit" or k == "crsf_token":
            continue
        form.__dict__['_fields'][k].render_kw = {'readonly': 'readonly'}

    if form.validate_on_submit():
        data = utils.prepare_data(request)
        rest.iface.purge_item(item_id, data)

        return redirect(url_for('items.index'))

    if form_only:
        html_form = render_template('items/item_remove_form.html',
                                    form=form, form_action=url_for('items.remove', item_id=item_id))
        return json.dumps({'html_form': html_form})

    return render_template('items/remove.html', form=form, form_action=url_for('items.remove', item_id=item_id))
