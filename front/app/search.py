from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField, RadioField, DateField
from wtforms.validators import ValidationError, NumberRange, Optional
import json
import jsonpickle

from .auth import login_required
from front.app import items, utils, rest


bp = Blueprint('search', __name__)


class SearchForm(FlaskForm):
    start_date = DateField('From', validators=[Optional()], default=utils.start_of_year, format="%Y-%m-%d")
    end_date = DateField('Until', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    submit = SubmitField('Search')


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def index():
    categories = utils.CategoryTypes()
    payments = utils.PaymentTypes()
    itemtypes = utils.ItemTypes()

    form = SearchForm()
    resolved_items = []
    if form.validate_on_submit():
        data_keys = ["description", "start_date", "end_date"]
        data = {}
        for key in request.form.keys():
            if key not in data_keys:
                continue
            if request.form[key]:
                val = request.form[key]
                if key in ["category", 'payment']:
                    val = json.loads(val)
                data[key] = val
        data['order_by'] = 'date'

        raw = rest.iface.get_items(data)
        resolved_items = items.resolve_items2(raw, itemtypes, payments, categories)
        redirect(url_for('search.index'))

    return render_template('search/search.html', items=resolved_items, form=form)
