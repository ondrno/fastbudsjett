from flask import (
    Blueprint, render_template
)
from ..auth.controllers import login_required
from ..utils import utils, rest

mod_categories = Blueprint('categories', __name__, url_prefix="/categories")


@mod_categories.route('/', methods=['GET'])
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

    return render_template('categories/index.html', categories=categories)

