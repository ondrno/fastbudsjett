from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
from flask_wtf import FlaskForm
from wtforms.fields import HiddenField
from wtforms import DecimalField, SelectMultipleField, StringField, SubmitField, RadioField, DateField
from wtforms.validators import ValidationError, NumberRange, Optional
import json
import jsonpickle
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
    # category = SelectMultipleField('Category', validators=[Optional()])
    # payment = SelectMultipleField('Payment', validators=[Optional()])
    submit = SubmitField('Search')


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def index():
    categories = jsonpickle.decode(session["categories"])
    payments = jsonpickle.decode(session["payments"])
    itemtypes = jsonpickle.decode(session["itemtypes"])

    year, month = items.get_year_month_from_url(session["selected_month"])

    form = SearchForm()
    form.start_date.default = f"{year}-{month:02}-01"

    resolved_items = {}
    print(request.form)
    for key in request.form.keys():
        print(key, request.form[key])
    if form.validate_on_submit():
        data_keys = ["description", "min_val", "max_val", "category", "payment", "start_date", "end_date"]
        data = {}
        for key in request.form.keys():
            if key not in data_keys:
                continue
            if request.form[key]:
                val = request.form[key]
                if key in ["category", 'payment']:
                    val = json.loads(val)
                data[key] = val
        if 'start_date' not in data and 'end_date' not in data:
            # if no start and no end is given, limit the search to start from the current month
            year, month = items.get_year_month_from_url(session["selected_month"])
            data['start_date'] = f"{year}-{month:02}-01"
        data['order_by'] = 'date'

        print(data)
        raw = rest.iface.get_items(data)
        resolved_items = items.resolve_items(raw, itemtypes, payments, categories)

        redirect(url_for('search.index'))

    return render_template('search/search.html', items=resolved_items, form=form)


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
