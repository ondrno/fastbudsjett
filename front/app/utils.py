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


def set_form_field_default(request, field, lookup, default: str):
    """
    set the default of a select/radio field dynamically,
    c.f. https://stackoverflow.com/questions/5519729/wtforms-how-to-select-options-in-selectmultiplefield/5519971#5519971

    Example: set_form_field_default(form.payment_type, 'cash')
    """
    field.choices = [(k, v) for k, v in lookup.items()]
    default_value = [k for (k, v) in field.choices if v == default]
    if default_value:
        field.default = default_value[0]
        field.process(request.form)

