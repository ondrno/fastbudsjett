from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import DecimalField, SelectMultipleField, StringField, SubmitField, RadioField
from wtforms.validators import ValidationError, NumberRange, Optional


from .auth import login_required
from . import items, utils, rest

bp = Blueprint('search', __name__)


class SearchForm(FlaskForm):
    start_date = DateField('From', validators=[Optional()])
    end_date = DateField('To', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    payment = SelectMultipleField('Payment', coerce=int)
    min_val = DecimalField('Amount min', validators=[Optional()])
    max_val = DecimalField('Amount max', validators=[Optional()])
    category = SelectMultipleField('Category', coerce=int)
    submit = SubmitField('Search')


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def index():
    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    form = SearchForm()
    utils.set_form_field_default(request, form.payment, payments_lookup, 'cash')
    utils.set_form_field_default(request, form.category, categories_lookup, 'food')

    payments = {}
    print(form)
    print(request.form)
    for i in request.form.keys():
        print(i, request.form[i])
    print(form.validate())
    print(form.validate_on_submit())
    if form.validate_on_submit():
        data_keys = ["description", "min_val", "max_val"]
        data = {}
        for i in request.form.keys():
            print(i)
            if i not in data_keys:
                continue
            if request.form[i]:
                data[i] = request.form[i]
        data['order_by'] = 'date'

        print(data)
        raw = rest.iface.get_items(data)
        payments = items.resolve_items(raw, itemtypes_lookup, payments_lookup, categories_lookup)

        redirect(url_for('search.index'))

    return render_template('search/search.html', items=payments, form=form)
