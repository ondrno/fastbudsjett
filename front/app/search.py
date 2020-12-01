from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
)
import operator
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length


from .auth import login_required
from . import items
from . import categories
from . import payment_types

bp = Blueprint('search', __name__)


class SearchForm(FlaskForm):
    description = StringField('Description', validators=[
        InputRequired(),
    ])
    submit = SubmitField('Search')


@bp.route('/search', methods=['POST'])
@login_required
def index():
    form = SearchForm()

    categories_lookup = categories.get_categories()
    payments_lookup = payment_types.get_payments()

    payments = items.get_items_and_resolve(payments_lookup, categories_lookup)

    return render_template('search/search.html', items=payments, form=form)
