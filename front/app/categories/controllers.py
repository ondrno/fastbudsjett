from flask import (
    Blueprint, render_template, session, request, jsonify
)
from ..auth.controllers import login_required
from ..utils import utils, rest
from .forms import CategoriesForm
import json

mod_categories = Blueprint('categories', __name__, url_prefix="/categories")


@mod_categories.route('/', methods=['GET'])
@login_required
def index():
    t = utils.types_from_session()
    itemtypes = t["itemtypes"]

    if utils.is_form_only(request) and 'itemtype_id' in request.args:
        # c.f. https://stackoverflow.com/questions/70474485/how-do-i-implement-dynamic-dependent-change-of-dropdown-select-options-using-py/70482570#70482570
        itemtype_id = int(request.args['itemtype_id'])
        income_id = itemtypes.get_id_for_income()
        if itemtypes.get_id_for_income() == itemtype_id:
            categories = t["income_categories"]
        else:
            categories = t["expense_categories"]
        return jsonify(categories.get_tuples_as_list())

    all_categories = {}
    income_id = itemtypes.get_id_for_income()
    expense_id = itemtypes.get_id_for_expense()
    all_categories[income_id] = t["income_categories"].get_tuples_as_list()
    all_categories[expense_id] = t["expense_categories"].get_tuples_as_list()

    print(f"categories/index(): categories={all_categories}")
    print(f"categories/index(): itemtypes={itemtypes}")
    return render_template('categories/index.html', itemtypes=itemtypes.get_tuples_as_list(), categories=all_categories)
