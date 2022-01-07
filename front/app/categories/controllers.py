from flask import (
    Blueprint, render_template, session
)
from ..auth.controllers import login_required
from ..utils import rest

mod_categories = Blueprint('categories', __name__, url_prefix="/categories")


@mod_categories.route('/', methods=['GET'])
@login_required
def index():
    all_categories = {}
    all_itemtypes = rest.iface.get_itemtypes()
    for i in all_itemtypes:
        data = dict()
        item_type_id = i['id']
        data['itemtype_id'] = item_type_id
        data['order_by'] = f'title_{session["locale"]}'
        my_categories = rest.iface.get_categories(data=data)
        all_categories[item_type_id] = my_categories

    print(f"categories={all_categories}")
    print(f"itemtypes={all_itemtypes}")
    return render_template('categories/index.html', itemtypes=all_itemtypes, categories=all_categories)
