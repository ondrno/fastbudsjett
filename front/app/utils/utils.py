from front.app.auth import login_required
from front.app import rest


class BaseTypes:
    def __init__(self, callback=None, items: dict = None):
        if items is None:
            items = {}
        self.items = items
        self.rest_callback = callback
        if not items and callback:
            self.items = self.fetch()

    def fetch(self) -> dict:
        """
        Get the name and id from the database using the callback from rest.iface.xxx
        and return a dictionary, e.g. itemtypes = { 2: 'revenue', 3: 'expenditure' }

        Example: categories_lookup = get_and_resolve(rest.iface.get_categories)
        """
        raw = self.rest_callback()
        items = {}
        raw = sorted(raw, key=lambda i: i['name'])
        for p in raw:
            id = p['id']
            name = p['name']
            items[id] = name
        return items

    def get_tuples_as_list(self):
        """ return a list of (key, value) pairs, e.g. [(1, 'a'), (2, 'b')] """
        return [(k, v) for k, v in self.items.items()]

    def get_key(self, val: str) -> int:
        for key, value in self.items.items():
            if val == value:
                return key
        return 0

    def get_value(self, key: int) -> str:
        if key in self.items:
            return self.items[key]
        else:
            return ''


class CategoryTypes(BaseTypes):
    """ """
    def __init__(self, callback=None, items: dict = None):
        if callback is None:
            callback = rest.iface.get_categories
        super().__init__(callback, items)


class ItemTypes(BaseTypes):
    def __init__(self, callback=None, items: dict = None):
        if callback is None:
            callback = rest.iface.get_itemtypes
        super().__init__(callback, items)


class PaymentTypes(BaseTypes):
    def __init__(self, callback=None, items: dict = None):
        if callback is None:
            callback = rest.iface.get_payments
        super().__init__(callback, items)


def set_form_field_default(request, field, lookup: BaseTypes, default: str):
    """
    set the default of a select/radio field dynamically,
    c.f. https://stackoverflow.com/questions/5519729/wtforms-how-to-select-options-in-selectmultiplefield/5519971#5519971

    Example: set_form_field_default(form.payment_type, 'cash')
    """
    field.choices = lookup.get_tuples_as_list()
    default_value = [k for (k, v) in field.choices if v == default]
    if default_value:
        field.default = default_value[0]
        field.process(request.form)