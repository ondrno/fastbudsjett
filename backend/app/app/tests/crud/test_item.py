from sqlalchemy.orm import Session
import datetime
import pytest
import mock
from alchemy_mock.mocking import AlchemyMagicMock

from app import crud
from app.db.exc import DBException
from app.schemas.item import ItemCreate, ItemUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_string, random_float


DESCRIPTION = random_string()
AMOUNT = random_float()
DATE = "01.12.2020"


def _compare_items(a, b):
    assert a.description == b.description
    assert a.amount == b.amount
    assert a.date == b.date
    assert a.payment_id == b.payment_id
    assert a.category_id == b.category_id
    assert a.id == b.id
    assert a.owner_id == b.owner_id


def _create_schema_for_item(category_id: int, payment_id: int) -> ItemCreate:
    return ItemCreate(description=DESCRIPTION, amount=AMOUNT, date=DATE, category_id=category_id, payment_id=payment_id)


def _create_item(db: Session, category_id: int, payment_id: int, user_id: int):
    item_in = _create_schema_for_item(category_id, payment_id)
    return crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user_id)


def test_create_item(db: Session, test_category, test_payment) -> None:
    user = create_random_user(db)
    item = _create_item(db, test_category.id, test_payment.id, user.id)
    assert item.description == DESCRIPTION
    assert item.amount == AMOUNT
    assert item.date == datetime.date(2020, 12, 1)
    assert item.payment_id == test_payment.id
    assert item.category_id == test_category.id
    assert item.owner_id == user.id


def test_create_item_invalid_payment_id_raises_exception(db: Session, test_category) -> None:
    user = create_random_user(db)
    with pytest.raises(DBException):
        _create_item(db, test_category.id, -1, user.id)


def test_create_item_invalid_category_id_raises_exception(db: Session, test_payment) -> None:
    user = create_random_user(db)
    with pytest.raises(DBException):
        _create_item(db, -1, test_payment.id, user.id)


def test_get_item(db: Session, test_category, test_payment) -> None:
    user = create_random_user(db)
    item = _create_item(db, test_category.id, test_payment.id, user.id)

    stored_item = crud.item.get(db=db, id=item.id)
    assert stored_item
    _compare_items(item, stored_item)


def test_get_item_with_invalid_id_returns_none(db: Session, test_category, test_payment) -> None:
    stored_item = crud.item.get(db=db, id=-1)
    assert stored_item is None


def test_update_item(db: Session, test_category, test_payment) -> None:
    user = create_random_user(db)
    item = _create_item(db, test_category.id, test_payment.id, user.id)

    description2 = random_string()
    item_update = ItemUpdate(description=description2)
    item2 = crud.item.update(db=db, db_obj=item, obj_in=item_update)
    _compare_items(item, item2)


def test_update_item_invalid_category_id_raises_exception(db: Session, test_category, test_payment) -> None:
    user = create_random_user(db)
    item = _create_item(db, test_category.id, test_payment.id, user.id)

    with pytest.raises(DBException):
        item_update = ItemUpdate(category_id=-1)
        crud.item.update(db=db, db_obj=item, obj_in=item_update)


def test_update_item_invalid_payment_id_raises_exception(db: Session, test_category, test_payment) -> None:
    user = create_random_user(db)
    item = _create_item(db, test_category.id, test_payment.id, user.id)

    with pytest.raises(DBException):
        item_update = ItemUpdate(payment_id=-1)
        crud.item.update(db=db, db_obj=item, obj_in=item_update)


def test_delete_item(db: Session, test_category, test_payment) -> None:
    user = create_random_user(db)
    item = _create_item(db, test_category.id, test_payment.id, user.id)

    item2 = crud.item.remove(db=db, id=item.id)
    item3 = crud.item.get(db=db, id=item.id)
    assert item3 is None
    _compare_items(item, item2)


def test_delete_item_with_invalid_id_raises_exception(db: Session, test_category, test_payment) -> None:
    with pytest.raises(DBException):
        crud.item.remove(db=db, id=-1)


class TestGetMulti:
    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_owner(self, mock_text):
        db_session = AlchemyMagicMock()
        owner_id = 1
        crud.item.get_multi(db=db_session, owner_id=owner_id)
        mock_text.assert_has_calls([
            mock.call(f"Item.owner_id == {owner_id}")
        ])
        db_session.query.assert_called()

    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_description(self, mock_text):
        db_session = AlchemyMagicMock()
        description = "Spar:"
        crud.item.get_multi(db=db_session, description=description)
        mock_text.assert_has_calls([
            mock.call(f"Item.description like '%{description}%'"),
        ])
        db_session.query.assert_called()

    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_description_and_owner(self, mock_text):
        db_session = AlchemyMagicMock()
        description = "Spar:"
        owner_id = 1
        crud.item.get_multi(db=db_session, description=description, owner_id=owner_id)
        mock_text.assert_has_calls([
            mock.call(f"Item.description like '%{description}%' AND Item.owner_id == {owner_id}"),
        ])
        db_session.query.assert_called()

    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_min_val(self, mock_text):
        db_session = AlchemyMagicMock()
        min_val = -3.45
        crud.item.get_multi(db=db_session, min_val=min_val)
        mock_text.assert_has_calls([
            mock.call(f"Item.amount >= {min_val}"),
        ])
        db_session.query.assert_called()

    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_max_val(self, mock_text):
        db_session = AlchemyMagicMock()
        max_val = 60.00
        crud.item.get_multi(db=db_session, max_val=max_val)
        mock_text.assert_has_calls([
            mock.call(f"Item.amount <= {max_val}"),
        ])
        db_session.query.assert_called()

    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_min_and_max_val(self, mock_text):
        db_session = AlchemyMagicMock()
        max_val = 60.00
        min_val = -3.45
        crud.item.get_multi(db=db_session, min_val=min_val, max_val=max_val)
        mock_text.assert_has_calls([
            mock.call(f"Item.amount >= {min_val} AND Item.amount <= {max_val}"),
        ])
        db_session.query.assert_called()

    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_start_and_end_date(self, mock_text):
        db_session = AlchemyMagicMock()
        start_date = "2020-01-20"
        end_date = "2020-01-27"
        crud.item.get_multi(db=db_session, start_date=start_date, end_date=end_date)
        mock_text.assert_has_calls([
            mock.call(f"Item.date >= '{start_date}' AND Item.date <= '{end_date}'"),
        ])
        db_session.query.assert_called()

    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_category_and_payment(self, mock_text):
        db_session = AlchemyMagicMock()
        category = [1]
        payment = [3, 4]
        crud.item.get_multi(db=db_session, category=category, payment=payment)
        mock_text.assert_has_calls([
            mock.call(f"Item.category_id in (1) AND Item.payment_id in (3,4)"),
        ])
        db_session.query.assert_called()

    @pytest.mark.parametrize("order", ["id", "description", "date",
                                       "created_at", "modified_at", "amount",
                                       "owner_id", "category_id", "payment_id"])
    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_category_and_valid_order_by(self, mock_text, order):
        db_session = AlchemyMagicMock()
        category = [1]
        crud.item.get_multi(db=db_session, category=category, order_by=order)
        mock_text.assert_has_calls([
            mock.call(f"Item.category_id in (1)"),
            mock.call(f"Item.{order}"),
        ])
        db_session.query.assert_called()

    @pytest.mark.parametrize("order", ["pid", "desc"])
    @mock.patch('app.crud.crud_item.text')
    def test_get_multi_with_invalid_order_by_uses_default(self, mock_text, order):
        db_session = AlchemyMagicMock()
        crud.item.get_multi(db=db_session, order_by=order)
        mock_text.assert_has_calls([
            mock.call(f"Item.id"),
        ])
        db_session.query.assert_called()
