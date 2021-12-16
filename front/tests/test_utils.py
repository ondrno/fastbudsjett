from front.app.utils import utils
from front.app.utils.rest import iface
import mock
import pytest
import datetime
from freezegun import freeze_time

# to be used for functions which use the @login_required decorator
# app.config['LOGIN_DISABLED'] = True


class TestBaseTypes:
    @mock.patch('front.app.utils.BaseTypes.fetch')
    def test_init_calls_nothing(self, mock_fetch):
        b = utils.BaseTypes()
        mock_fetch.assert_not_called()

    def callback(self):
        pass

    @mock.patch('front.app.utils.BaseTypes.fetch')
    def test_init_calls_callback(self, mock_fetch):
        items = {1: 'a'}
        mock_fetch.return_value = items
        b = utils.BaseTypes(callback=self.callback)
        assert b.items == items
        mock_fetch.assert_called_once()

    def test_get_key_returns_key(self):
        items = {1: 'a'}
        b = utils.BaseTypes(callback=None, items=items)
        assert b.get_key('a') == 1

    def test_get_key_returns_zero_if_no_key(self):
        items = {1: 'a'}
        b = utils.BaseTypes(callback=None, items=items)
        assert b.get_key('b') == 0

    def test_get_key_returns_zero_if_no_key_and_no_init(self):
        b = utils.BaseTypes()
        assert b.get_key('b') == 0

    def test_get_value_returns_value(self):
        items = {1: 'a'}
        b = utils.BaseTypes(callback=None, items=items)
        assert b.get_value(1) == 'a'

    def test_get_value_returns_empty_string(self):
        items = {'1': 'a'}
        b = utils.BaseTypes(callback=None, items=items)
        assert b.get_value('2') == ''

    def test_get_value_returns_str_if_int_not_found(self):
        def produce():
            return [{'id': 1, 'title_en': 'a'}, {'id': 2, 'title_en': 'b'}]
        b = utils.BaseTypes(callback=produce)
        assert b.get_value(2) == 'b'
        assert b.get_value('2') == 'b'

    def test_get_tuples_as_list(self):
        items = {'1': 'a', '2': "b"}
        b = utils.BaseTypes(callback=None, items=items)
        assert b.get_tuples_as_list() == [('1', 'a'), ('2', 'b')]


@pytest.fixture(autouse=True)
def clear_lru_cache():
    # this fixture is required to test functions with the @lru_cache decorator
    iface.get_categories.cache_clear()
    iface.get_payments.cache_clear()
    iface.get_itemtypes.cache_clear()
    yield
    iface.get_categories.cache_clear()
    iface.get_payments.cache_clear()
    iface.get_itemtypes.cache_clear()


@mock.patch('front.app.utils.BaseTypes.fetch')
def test_init_category_types_class(mock_fetch):
    c = utils.CategoryTypes()
    assert c.rest_callback == iface.get_categories


@mock.patch('front.app.utils.BaseTypes.fetch')
def test_init_payment_types_class(mock_fetch):
    c = utils.PaymentTypes()
    assert c.rest_callback == iface.get_payments


@mock.patch('front.app.utils.BaseTypes.fetch')
def test_init_item_types_class(mock_fetch):
    c = utils.ItemTypes()
    assert c.rest_callback == iface.get_itemtypes


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
