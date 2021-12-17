from flask import (
    request, session
)
import datetime
from dateutil.relativedelta import relativedelta
import jsonpickle
from ..utils import rest


class BaseTypes:
    def __init__(self, callback=None, entries: dict = None, locale: str = None):
        if entries is None:
            entries = {}
        if locale is None:
            locale = session.get('locale', 'en')
        self.entries = entries
        self.locale = locale
        self.default_locale = 'en'
        self.rest_callback = callback
        if not entries and callback:
            self.entries = self.fetch()

    def fetch(self) -> dict:
        """
        Get the title_en, title_de and id from the database using the callback from rest.iface.xxx
        and return a dictionary, e.g. itemtypes = { '2': {title_en: 'income', title_de: 'Einnahme'},
                                                    '3': {title_en: 'expense', title_de: 'Ausgabe'} }
        """
        raw = self.rest_callback()
        entries = {}
        for p in raw:
            id_ = str(p['id'])
            title_de = p['title_de']
            title_en = p['title_en']
            entries[id_] = {'title_de': title_de, 'title_en': title_en}
        return entries

    def _get_title(self, all_titles: dict, locale: str = None) -> str:
        if not locale:
            locale = self.locale
        localized_key = f"title_{locale}"
        default_key = f"title_{self.default_locale}"
        if localized_key in all_titles:
            return all_titles[localized_key]
        else:
            return all_titles[default_key]

    def get_tuples_as_list(self, locale: str = None):
        """ return a list of localized (id, title) pairs, e.g. [('1', 'income'), ('2', 'expense')] """
        result = []
        for _id, _all_titles in self.entries.items():
            title = self._get_title(_all_titles, locale)
            result.append((_id, title))
        return result

    def get_id_for_title(self, title: str) -> int:
        for _id, _all_titles in self.entries.items():
            if title in _all_titles.values():
                return int(_id)
        return 0

    def get_title_for_id(self, id_: str, locale: str = None) -> str:
        id_ = str(id_)
        result = ''
        if id_ in self.entries:
            all_titles = self.entries[id_]
            result = self._get_title(all_titles, locale)
        return result


class CategoryTypes(BaseTypes):
    """ """
    def __init__(self, callback=None, entries: dict = None, locale: str = None):
        if callback is None:
            callback = rest.iface.get_categories
        super().__init__(callback, entries, locale)


class ItemTypes(BaseTypes):
    def __init__(self, callback=None, entries: dict = None, locale: str = None):
        if callback is None:
            callback = rest.iface.get_itemtypes
        super().__init__(callback, entries, locale)


class PaymentTypes(BaseTypes):
    def __init__(self, callback=None, entries: dict = None, locale: str = None):
        if callback is None:
            callback = rest.iface.get_payments
        super().__init__(callback, entries, locale)


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
