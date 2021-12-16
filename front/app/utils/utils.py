from flask import (
    request, session
)
import datetime
from dateutil.relativedelta import relativedelta
import jsonpickle
from ..utils import rest


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
        Get the title_en and id from the database using the callback from rest.iface.xxx
        and return a dictionary, e.g. itemtypes = { '2': 'income', '3': 'expense' }

        Example: categories_lookup = get_and_resolve(rest.iface.get_categories)
        """
        raw = self.rest_callback()
        items = {}
        raw = sorted(raw, key=lambda i: i['title_en'])
        for p in raw:
            id = p['id']
            name = p['title_en']
            items[str(id)] = name
        return items

    def get_tuples_as_list(self):
        """ return a list of (key, value) pairs, e.g. [('1', 'a'), ('2', 'b')] """
        return [(k, v) for k, v in self.items.items()]

    def get_key(self, val: str) -> int:
        for key, value in self.items.items():
            if val == value:
                return key
        return 0

    def get_value(self, key: int) -> str:
        result = ''
        if key in self.items:
            result = self.items[key]
        else:
            key = str(key)
            result = self.items.get(key, '')
        return result


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
    if not default_value:
        default_value = str(default)
    # print(f"set_form_field_default={field} lu={lookup} default={default} choices={field.choices} -> default_value={default_value}")
    if default_value:
        field.default = default_value[0]
        field.process(request.form)


def end_of_month(month: int = None):
    today = datetime.datetime.today()
    if month is None:
        month = today.month
    d = (datetime.date(today.year, month, 1) + relativedelta(day=31))
    return d


def start_of_year():
    today = datetime.datetime.today()
    d = datetime.date(today.year, 1, 1)
    return d


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
