from .auth import login_required
from . import rest


@login_required
def get_categories(sort_by_name: bool = True):
    raw = rest.iface.get_categories()
    categories = {}
    if sort_by_name:
        raw = sorted(raw, key=lambda i: i['name'])
    for p in raw:
        id = p['id']
        name = p['name']
        categories[id] = name
    return categories
