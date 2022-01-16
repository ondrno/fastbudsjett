from front.app import app
from front.app.utils import utils
from front.app.utils.rest import iface
import mock
import pytest
import datetime
from freezegun import freeze_time

# to be used for functions which use the @login_required decorator
# app.config['LOGIN_DISABLED'] = True


def sample_callback(*args, **kwargs):
    items = [{'id': '1', 'title_en': 'income', 'title_de': 'Einnahme'}]
    for a in args:
        items.append(a)
    if kwargs:
        for k, v in kwargs.items():
            items.append(v)
    return items


class TestBaseTypes:
    @mock.patch('front.app.utils.BaseTypes.fetch')
    def test_init_calls_nothing(self, mock_fetch):
        utils.BaseTypes(locale='en')
        mock_fetch.assert_not_called()

    @mock.patch('front.app.utils.BaseTypes.fetch')
    def test_init_calls_fetch(self, mock_fetch):
        items = {'1': 'a'}
        mock_fetch.return_value = items
        b = utils.BaseTypes(callback=sample_callback, locale='en')
        assert b.entries == items
        mock_fetch.assert_called_once()

    def test_init_calls_callback_without_args(self):
        b = utils.BaseTypes(callback=sample_callback, locale='en')
        assert b.entries == {'1': {'title_de': 'Einnahme', 'title_en': 'income'}}
        assert b.kwargs == {}
        assert b.args == ()

    def test_init_calls_callback_with_single_kwargs(self):
        data = {'id': 2, 'title_en': 'ice', 'title_de': 'eis'}
        b = utils.BaseTypes(entries=None, locale='en', callback=sample_callback, data=data)
        assert b.entries == {'1': {'title_de': 'Einnahme', 'title_en': 'income'},
                             '2': {'title_en': 'ice', 'title_de': 'eis'}}
        assert b.kwargs == {'data': data}
        assert b.args == ()

    def test_init_calls_callback_with_single_args(self):
        data = {'id': 2, 'title_en': 'ice', 'title_de': 'eis'}
        b = utils.BaseTypes(None, 'en', sample_callback, data)
        assert b.entries == {'1': {'title_de': 'Einnahme', 'title_en': 'income'},
                             '2': {'title_en': 'ice', 'title_de': 'eis'}}
        assert b.kwargs == {}
        assert b.args == (data,)

    def test_init_calls_callback_with_args_and_kwargs(self):
        data = {'id': 2, 'title_en': 'ice', 'title_de': 'eis'}
        data3 = {'id': 3, 'title_en': 'ice', 'title_de': 'eis'}
        b = utils.BaseTypes(None, 'en', sample_callback, data, data3=data3)
        assert b.entries == {'1': {'title_de': 'Einnahme', 'title_en': 'income'},
                             '2': {'title_en': 'ice', 'title_de': 'eis'},
                             '3': {'title_en': 'ice', 'title_de': 'eis'}
                             }
        assert b.kwargs == {'data3': data3}
        assert b.args == (data,)

    def test_get_id_for_title_returns_title(self):
        items = {'1': {'title_en': 'a'}}
        b = utils.BaseTypes(callback=None, entries=items, locale='en')
        assert b.get_id_for_title('a') == 1

    def test_get_id_for_title_returns_title_for_all_locales(self):
        items = {'1': {'title_en': 'english', 'title_de': 'german'}}
        b = utils.BaseTypes(callback=None, entries=items, locale='en')
        assert b.get_id_for_title('german') == 1

    def test_get_id_for_title_returns_zero_if_no_matching_title(self):
        items = {'1': {'title_en': 'a'}}
        b = utils.BaseTypes(callback=None, entries=items, locale='en')
        assert b.get_id_for_title('b') == 0

    def test_get_id_for_title_returns_zero_if_no_entries(self):
        b = utils.BaseTypes(locale="en")
        assert b.get_id_for_title('b') == 0

    def test_get_title_for_id_returns_localized_en_title(self):
        items = {'1': {'title_en': 'english', 'title_de': 'german'}}
        b = utils.BaseTypes(callback=None, entries=items, locale="en")
        assert b.get_title_for_id(1) == 'english'

    def test_get_title_for_id_returns_localized_de_title(self):
        items = {'1': {'title_en': 'english', 'title_de': 'german'}}
        b = utils.BaseTypes(callback=None, entries=items, locale="de")
        assert b.get_title_for_id(1) == 'german'

    def test_get_value_returns_empty_string(self):
        items = {'1': {'title_en': 'english', 'title_de': 'german'}}
        b = utils.BaseTypes(callback=None, entries=items, locale="en")
        assert b.get_title_for_id(2) == ''

    def test_get_value_returns_str_if_int_not_found(self):
        def produce():
            return [{'id': 1, 'title_en': 'a', 'title_de': 'ag'}, {'id': 2, 'title_en': 'b', 'title_de': 'bg'}]
        b = utils.BaseTypes(callback=produce, locale="en")
        assert b.get_title_for_id('2', locale="de") == 'bg'
        assert b.get_title_for_id(2, locale="en") == 'b'

    def test_get_tuples_as_list_default_locale(self):
        items = {'1': {'title_en': 'uk', 'title_de': 'de'},
                 '2': {'title_en': 'en', 'title_de': 'german'}}
        b = utils.BaseTypes(callback=None, entries=items, locale="en")
        assert b.get_tuples_as_list() == [('1', 'uk'), ('2', 'en')]

    def test_get_tuples_as_list_specific_locale(self):
        items = {'1': {'title_en': 'uk', 'title_de': 'de'},
                 '2': {'title_en': 'en', 'title_de': 'german'}}
        b = utils.BaseTypes(callback=None, entries=items, locale="en")
        assert b.get_tuples_as_list(locale="de") == [('1', 'de'), ('2', 'german')]


class TestItemTypes:
    @mock.patch('front.app.utils.ItemTypes.fetch')
    def test_get_id_for_income_expense(self, mock_fetch):
        items = {'1': {'title_en': 'income', 'title_de': 'Einnahme'},
                 '2': {'title_en': 'expense', 'title_de': 'Ausgabe'}
                 }
        mock_fetch.return_value = items
        b = utils.ItemTypes(callback=sample_callback, locale='en')
        assert 1 == b.get_id_for_income()
        assert 2 == b.get_id_for_expense()

    def test_init_calls_callback_with_args_and_kwargs(self):
        data = {'id': 2, 'title_en': 'ice', 'title_de': 'eis'}
        data3 = {'id': 3, 'title_en': 'ice', 'title_de': 'eis'}
        b = utils.ItemTypes(None, 'en', sample_callback, data, data3=data3)
        assert b.entries == {'1': {'title_de': 'Einnahme', 'title_en': 'income'},
                             '2': {'title_en': 'ice', 'title_de': 'eis'},
                             '3': {'title_en': 'ice', 'title_de': 'eis'}
                             }
        assert b.kwargs == {'data3': data3}
        assert b.args == (data,)


@pytest.fixture(autouse=True)
def clear_lru_cache():
    # this fixture is required to test functions with the @lru_cache decorator
    # iface.get_categories.cache_clear()
    iface.get_payments.cache_clear()
    iface.get_itemtypes.cache_clear()
    yield
    # iface.get_categories.cache_clear()
    iface.get_payments.cache_clear()
    iface.get_itemtypes.cache_clear()


@mock.patch('front.app.utils.BaseTypes.fetch')
def test_init_category_types_class(mock_fetch):
    c = utils.CategoryTypes(locale="en")
    assert c.callback == iface.get_categories


@mock.patch('front.app.utils.BaseTypes.fetch')
def test_init_payment_types_class(mock_fetch):
    c = utils.PaymentTypes(locale="en")
    assert c.callback == iface.get_payments


@mock.patch('front.app.utils.BaseTypes.fetch')
def test_init_item_types_class(mock_fetch):
    c = utils.ItemTypes(locale="en")
    assert c.callback == iface.get_itemtypes


@pytest.mark.parametrize("year, month, exp_day", [(2021, 1, 31), (2021, 2, 28), (2021, 4, 30)])
def test_end_of_month(year, month, exp_day):
    exp_date = datetime.date(year, month, exp_day)
    with freeze_time(f"{year}-{month}-15"):
        d = utils.end_of_month(month)
    assert d.day == exp_day


@pytest.mark.parametrize("year, month, day", [(2021, 1, 31), (2021, 2, 28), (2021, 4, 15)])
def test_start_of_month(year, month, day):
    with freeze_time(f"{year}-{month}-{day}"):
        d = utils.start_of_year()
    assert d.day == 1
