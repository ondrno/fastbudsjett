from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
import re
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import DecimalField, SelectMultipleField, StringField, SubmitField, RadioField
from wtforms.validators import ValidationError


from .auth import login_required
from . import items, utils, rest

bp = Blueprint('search', __name__)


class SearchForm(FlaskForm):
    from_date = DateField('From')
    to_date = DateField('To')
    description = StringField('Description')
    payment_type = SelectMultipleField('Payment', coerce=int)
    amount = StringField('Amount')
    category = SelectMultipleField('Category', coerce=int)
    submit = SubmitField('Search')

    def validate(self):
        result = True
        if self.description.data:
            data = str(self.amount.data)
            # allow expressions like: >10, <10, >=20
            if not re.match(r'^([><]?=?\d+)?$', data):
                self.amount.errors.append('Invalid search pattern for amount')
                print("Validation error")
                raise ValidationError("Invalid input syntax")
                result = False

        return result

    def get_active_fields(self):
        active = set()
        for field in ['from_date', 'to_date', 'description',
                      'payment_type', 'amount', 'category']:
            if getattr(self, field):
                active.add(field)
        return active


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def index():
    categories_lookup = utils.get_categories()
    payments_lookup = utils.get_payments()
    itemtypes_lookup = utils.get_itemtypes()

    form = SearchForm()
    utils.set_form_field_default(request, form.payment_type, payments_lookup, 'cash')
    utils.set_form_field_default(request, form.category, categories_lookup, 'food')

    if form.validate_on_submit():
        fields = form.get_active_fields()
        print("active fields:", fields)
        # from_date = request.form['from_date']
        # to_date = request.form['to_date']
        # amount = request.form['amount']
        # category = request.form['category']
        # payment_type = request.form['payment_type']
        description = request.form['description']
        print(description)

        data = {'description': description, 'order_by': 'date'}
        raw = rest.iface.get_items(data)
        print(raw)
        payments = items.resolve_items(raw, itemtypes_lookup, payments_lookup, categories_lookup)

        # redirect(url_for('search.index'))

    return render_template('search/search.html', items=payments, form=form)
