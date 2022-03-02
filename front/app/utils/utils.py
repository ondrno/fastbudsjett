from flask import (
    request, session
)
import datetime
import calendar
from dateutil.relativedelta import relativedelta
import jsonpickle
from ..utils import rest


class BaseTypes:
    def __init__(self, entries: dict = None, locale: str = None, callback=None, *args, **kwargs):
        if entries is None:
            entries = {}
        if locale is None:
            locale = session.get('locale', 'en')
        self.entries = entries
        self.locale = locale
        self.default_locale = 'en'
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        if not entries and callback:
            self.entries = self.fetch()

    def fetch(self) -> dict:
        """
        Get the title_en, title_de and id from the database using the callback from rest.iface.xxx
        and return a dictionary, e.g. itemtypes = { '2': {title_en: 'income', title_de: 'Einnahme'},
                                                    '3': {title_en: 'expense', title_de: 'Ausgabe'} }
        """
        if 'data' in self.kwargs:
            raw = self.callback(data=self.kwargs['data'])
        else:
            raw = self.callback(*self.args, **self.kwargs)
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

    def get_tuples_as_dict(self, locale: str = None):
        """ return a dict {id: title}, e.g. {1: 'income', 2: 'expense'} """
        result = {}
        for _id, _all_titles in self.entries.items():
            title = self._get_title(_all_titles, locale)
            result[_id] = title
        return result

    def get_id_for_title(self, title: str) -> int:
        # print(f"get_id_for_title: self={self} title={title}, entries={self.entries.items()}")
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
    def __init__(self, entries: dict = None, locale: str = None, callback=None, *args, **kwargs):
        # print(f"category types entries={entries} locale={locale}, callback={callback}, args={args}, kwargs={kwargs}")
        if callback is None:
            callback = rest.iface.get_categories
        super().__init__(entries, locale, callback, *args, **kwargs)


class ItemTypes(BaseTypes):
    def __init__(self, entries: dict = None, locale: str = None, callback=None, *args, **kwargs):
        if callback is None:
            callback = rest.iface.get_itemtypes
        super().__init__(entries, locale, callback, *args, **kwargs)

    def get_id_for_income(self):
        return self.get_id_for_title(title='income')

    def get_id_for_expense(self):
        return self.get_id_for_title(title='expense')


class PaymentTypes(BaseTypes):
    def __init__(self, entries: dict = None, locale: str = None, callback=None, *args, **kwargs):
        if callback is None:
            callback = rest.iface.get_payments
        super().__init__(entries, locale, callback, *args, **kwargs)


def set_form_default(request, field, lookup: BaseTypes, default: int = 0):
    """
    set the default of a select/radio field dynamically,
    c.f. https://stackoverflow.com/questions/5519729/wtforms-how-to-select-options-in-selectmultiplefield/5519971#5519971
    """
    field.choices = lookup.get_tuples_as_list()
    if default == 0:
        default = get_form_default_id(field.choices)
    field.default = default
    field.process(request.form)
    # print(f"set_form_default: field={field} lu={lookup} default={default} choices={field.choices}")


def get_form_default_id(choices: list) -> int:
    # FIXME: nasty hack, better have a field 'is_default' in database
    # print("--------------------------------")
    for i in choices:
        # print(f"get_form_default_id: {i}")
        default = i[0]
        if i[1] in ['food', 'Essen'] or \
           i[1] in ['salary', 'Gehalt'] or \
           i[1] in ['expense', 'Ausgabe'] or \
           i[1] in ['cash', 'bar']:
            # print(f"get_form_default: {i[1]} -> {i[0]}")
            return default


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


def types_to_session(income_categories, expense_categories, payments, itemtypes):
    session["income_categories"] = jsonpickle.encode(income_categories)
    session["expense_categories"] = jsonpickle.encode(expense_categories)
    session["payments"] = jsonpickle.encode(payments)
    session["itemtypes"] = jsonpickle.encode(itemtypes)


def types_from_session() -> dict:
    return {
        'income_categories': jsonpickle.decode(session["income_categories"]),
        'expense_categories': jsonpickle.decode(session["expense_categories"]),
        'payments': jsonpickle.decode(session["payments"]),
        'itemtypes': jsonpickle.decode(session["itemtypes"]),
    }


def _get_full_locale(locale: str) -> str:
    # make sure that these locales are installed on system you are running the web application
    all_locale = {'en': 'en_GB.utf8', 'de': 'de_DE.utf8'}
    if locale in all_locale:
        return all_locale[locale]
    else:
        raise ValueError(f"Invalid locale={locale}")


def month_name(month_no: int, abbr: bool = False, locale: str = None) -> str:
    if locale is None:
        locale = session['locale']
    full_locale = _get_full_locale(locale)
    with calendar.different_locale(full_locale):
        if abbr:
            return calendar.month_abbr[month_no]
        else:
            return calendar.month_name[month_no]


def day_name(dow: int, abbr: bool = True, locale: str = None) -> str:
    if locale is None:
        locale = session['locale']
    full_locale = _get_full_locale(locale)
    with calendar.different_locale(full_locale):
        if abbr:
            return calendar.day_abbr[dow]
        else:
            return calendar.day_name[dow]


def is_form_only(r: request):
    return 'form_only' in request.args and request.method == 'GET'


def is_get_request(r: request):
    return request.method == 'GET'


def is_post_request(r: request):
    return request.method == 'POST'
