from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
from werkzeug.exceptions import abort

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
def index():
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

    return render_template('items/index.html', items=payments)
