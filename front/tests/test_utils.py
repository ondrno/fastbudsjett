from front.app.utils import utils
from front.app.rest import iface
from front.app import app
import mock
import pytest

# to be used for functions which use the @login_required decorator
# app.config['LOGIN_DISABLED'] = True


class TestBaseTypes:
    @mock.patch('front.app.utils.utils.get_and_resolve')
    def test_init_calls_nothing(self, mock_get):
        b = utils.BaseTypes()
        mock_get.assert_not_called()

    def callback(self):
        pass

    @mock.patch('front.app.utils.utils.get_and_resolve')
    def test_init_calls_callback(self, mock_get):
        items = {1: 'a'}
        mock_get.return_value = items
        b = utils.BaseTypes(callback=self.callback)
        assert b.items == items
        mock_get.assert_called_once()

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
        items = {1: 'a'}
        b = utils.BaseTypes(callback=None, items=items)
        assert b.get_value(2) == ''

    def test_get_tuples_as_list(self):
        items = {1: 'a', 2: "b"}
        b = utils.BaseTypes(callback=None, items=items)
        assert b.get_tuples_as_list() == [(1, 'a'), (2, 'b')]


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


@mock.patch('front.app.utils.utils.get_and_resolve')
def test_init_category_types_class(mock_get):
    utils.CategoryTypes()
    mock_get.assert_called_once_with(iface.get_categories)


@mock.patch('front.app.utils.utils.get_and_resolve')
def test_init_payment_types_class(mock_get):
    utils.PaymentTypes()
    mock_get.assert_called_once_with(iface.get_payments)


@mock.patch('front.app.utils.utils.get_and_resolve')
def test_init_item_types_class(mock_get):
    utils.ItemTypes()
    mock_get.assert_called_once_with(iface.get_itemtypes)
