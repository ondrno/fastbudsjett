from flask import (
    Blueprint, g, redirect, render_template, request, url_for, session
)
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, NumberRange
import datetime
import calendar
from dateutil.relativedelta import relativedelta
import json
import jsonpickle

from .auth import login_required
from . import rest
from front.app.utils import utils


bp = Blueprint('categories', __name__)


class CategoriesForm(FlaskForm):
    name = StringField('Description', validators=[
        InputRequired(),
        Length(5, 30)
    ])
    itemtype = SelectField('ItemType', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Create')

def prepare_data(r: request):
    data = {'date': r.form['date'],
            'amount': r.form['amount'],
            'category_id': r.form['category'],
            'payment_id': r.form['payment_type'],
            'description': r.form['description'],
            'itemtype_id': r.form['itemtype']
            }
    return data


def types_to_session(categories, payments, itemtypes):
    session["categories"] = jsonpickle.encode(categories)
    session["payments"] = jsonpickle.encode(payments)
    session["itemtypes"] = jsonpickle.encode(itemtypes)


def types_from_session() -> dict:
    return {
        'categories': jsonpickle.decode(session["categories"]),
        'payments': jsonpickle.decode(session["payments"]),
        'itemtypes': jsonpickle.decode(session["itemtypes"]),
    }


@bp.route('/categories', methods=['GET'])
@login_required
def index():
    all_categories = rest.iface.get_categories()
    itemtypes = utils.ItemTypes()
    categories = {}
    for c in all_categories:
        itemtype_id = c['itemtype_id']
        itemtype_name = itemtypes.get_value(itemtype_id)
        c['itemtype_name'] = itemtype_name
        if itemtype_name not in categories:
            categories[itemtype_name] = []
        categories[itemtype_name].append(c)

    print(categories)

    return render_template('categories/index.html', categories=categories)

