from .auth import login_required
from . import rest


@login_required
def get_categories(sort_by_name: bool = True):
    return _get_x_and_resolve(rest.iface.get_categories, sort_by_name)


@login_required
def get_payments(sort_by_name: bool = True):
    return _get_x_and_resolve(rest.iface.get_payments, sort_by_name)


@login_required
def get_itemtypes(sort_by_name: bool = True):
    return _get_x_and_resolve(rest.iface.get_itemtypes, sort_by_name)


def _get_x_and_resolve(callback, sort_by_name: bool = True) -> dict:
    """
    Get the name and id from the database using the callback from rest.iface.xxx
    and return a dictionary, e.g. itemtypes = { 2: 'revenue', 3: 'expenditure' }

    Example: categories_lookup = get_x_and_resolve(rest.iface.get_categories)
    """
    raw = callback()
    items = {}
    if sort_by_name:
        raw = sorted(raw, key=lambda i: i['name'])
    for p in raw:
        id = p['id']
        name = p['name']
        items[id] = name
    return items
