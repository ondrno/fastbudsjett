from flask import (
    Blueprint, redirect, render_template, request, url_for, )
import json
from ..auth.controllers import login_required
from .. import items, utils
from ..utils import rest
from .forms import SearchForm


mod_search = Blueprint('search', __name__, url_prefix="/search")


@mod_search.route('/', methods=['GET', 'POST'])
@login_required
def index():
    t = utils.types_from_session()
    income_categories = t["income_categories"]
    expense_categories = t["expense_categories"]
    payments = t["payments"]
    itemtypes = t["itemtypes"]

    form = SearchForm()
    resolved_items = {}
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
        resolved_items = items.resolve_items(raw, itemtypes, payments, income_categories, expense_categories)
        # print(f"resolved items={resolved_items}")
        redirect(url_for('search.index'))

    return render_template('search/search.html', items=resolved_items, form=form)
