from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
import re
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import DecimalField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import ValidationError


from .auth import login_required
from . import items
from . import categories
from . import payment_types

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
            if not re.match(r'^[><]?=?\d+$', data):
                self.amount.errors.append('Invalid search pattern for amount')
                print("Validation error")
                raise ValidationError("Invalid input syntax")
                result = False

        return result

    def get_active_fields(self):
        active = set()
        for field in [self.from_date, self.to_date, self.description,
                      self.payment_type, self.amount, self.category]:
            if self.field.data:
                active.add(field)
        return active


@bp.route('/search', methods=['POST', 'GET'])
@login_required
def index():
    form = SearchForm()

    categories_lookup = categories.get_categories()
    payments_lookup = payment_types.get_payments()

    form.payment_type.choices = [(k, v) for k, v in payments_lookup.items()]
    form.category.choices = [(k, v) for k, v in categories_lookup.items()]

    # print(form.get_active_fields())
    payments = items.get_items_and_resolve(payments_lookup, categories_lookup)


    return render_template('search/search.html', items=payments, form=form)
