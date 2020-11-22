from sqlalchemy.orm import Session
import datetime
import pytest

from app import crud
from app.db.exc import DBException
from app.schemas.item import ItemCreate, ItemUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_string, random_float


DESCRIPTION = random_string()
AMOUNT = random_float()
DATE = "01.12.2020"


def _compare_items(a: ItemCreate, b: ItemCreate):
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
