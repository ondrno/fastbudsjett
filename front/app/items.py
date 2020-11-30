from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
import operator

from .auth import login_required
from . import rest

bp = Blueprint('items', __name__)


def get_categories():
    raw = rest.iface.get_categories()
    categories = {}
    for p in raw:
        id = p['id']
        name = p['name']
        categories[id] = name
    return categories


def get_payments():
    raw = rest.iface.get_payments()
    payments = {}
    for p in raw:
        id = p['id']
        name = p['name']
        payments[id] = name
    return payments


@bp.route('/')
@login_required
def index():
    # if request.method == 'POST':
    #     date = request.form['inputDate']
    #     amount = request.form['inputAmount']
    #     category = request.form['inputCategory']
    #     payment = request.form['inputPayment']
    #     description = request.form['inputDescription']
    #     # TODO
    categories_lookup = get_categories()
    payments_lookup = get_payments()

    payments_raw = rest.iface.get_items()
    payments = []
    for i in payments_raw:
        cat_id = i['category_id']
        payment_id = i['payment_id']

        payment = i
        payment['payment'] = payments_lookup.get(payment_id)
        payment['category'] = categories_lookup.get(cat_id)
        payments.append(payment)

    categories_sorted = {}
    for k, v in sorted(categories_lookup.items(), key=operator.itemgetter(1)):
        categories_sorted[k] = {'name': v}
        if v.lower() == 'food':
            categories_sorted[k]['selected'] = True

    print(categories_sorted.items())

    payments_sorted = {}
    for k, v in sorted(payments_lookup.items(), key=operator.itemgetter(1)):
        payments_sorted[k] = {'name': v}
        if v.lower() == 'cash':
            payments_sorted[k]['selected'] = True

    print(payments_sorted.items())

    return render_template('items/index.html',
                           items=payments,
                           categories=categories_sorted,
                           payments=payments_sorted)
