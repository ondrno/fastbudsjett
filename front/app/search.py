from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.fields import HiddenField
from wtforms import DecimalField, SelectMultipleField, StringField, SubmitField, RadioField
from wtforms.validators import ValidationError, NumberRange, Optional
import json
from functools import lru_cache

from .auth import login_required
from . import items, utils, rest

bp = Blueprint('search', __name__)


class SearchForm(FlaskForm):
    start_date = DateField('From', validators=[Optional()])
    end_date = DateField('To', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    min_val = DecimalField('Amount min', validators=[Optional()])
    max_val = DecimalField('Amount max', validators=[Optional()])
    category = HiddenField('Category', validators=[Optional()])
    payment = HiddenField('Payment', validators=[Optional()])
    submit = SubmitField('Search')


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def index():
    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    form = SearchForm()

    payments = {}
    print(request.form)
    for i in request.form.keys():
        print(i, request.form[i])
    print(form.validate())
    print(form.validate_on_submit())
    if form.validate_on_submit():
        data_keys = ["description", "min_val", "max_val", "category", "payment"]
        data = {}
        for i in request.form.keys():
            print(i)
            if i not in data_keys:
                continue
            if request.form[i]:
                val = request.form[i]
                if i in ["category", 'payment']:
                    val = json.loads(val)
                data[i] = val
        data['order_by'] = 'date'

        print(data)
        raw = rest.iface.get_items(data)
        payments = items.resolve_items(raw, itemtypes_lookup, payments_lookup, categories_lookup)

        redirect(url_for('search.index'))

    return render_template('search/search.html', items=payments, form=form)


@bp.route('/search/get_categories', methods=['POST'])
@login_required
def get_categories():
    categories_lookup = utils.get_categories()
    data = []
    for k, v in categories_lookup.items():
        data.append({'id': k, 'name': v})
    return {'results': data}


@bp.route('/search/get_payments', methods=['POST'])
@login_required
def get_payments():
    payments_lookup = utils.get_payments()
    data = []
    for k, v in payments_lookup.items():
        data.append({'id': k, 'name': v})
    return {'results': data}
