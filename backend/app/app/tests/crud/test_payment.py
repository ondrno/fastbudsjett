from sqlalchemy.orm import Session
import mock
import pytest
from random import randint

from app import crud
from app.db.exc import DBException
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.schemas.item import ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_string


def _create_schema_for_payment(name) -> ItemCreate:
    return PaymentCreate(name=name)


def _create_payment(db: Session, name: str):
    payment_in = _create_schema_for_payment(name)
    return crud.payment.create(db=db, obj_in=payment_in)


def _compare_entries(a, b):
    assert a.name == b.name
    assert a.id == b.id
    assert a.items == b.items


def test_create_payment(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    payment = _create_payment(db, name=name)
    assert payment.name == name
    assert payment.items == []


def test_payment_items_field_is_propagated_by_items(db: Session, test_category) -> None:
    name = random_string(length=randint(3, 30))
    payment = _create_payment(db, name=name)
    assert payment.name == name
    assert payment.items == []

    itemtype = mock.MagicMock()
    user = create_random_user(db)
    item_in = ItemCreate(description="test_description", amount="12.20", date="01.01.2020",
                         payment_id=payment.id, category_id=test_category.id, itemtype_id=itemtype.id)
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user.id)
    assert payment.items == [item]

    crud.item.remove(db=db, id=item.id)
    assert payment.items == []


def test_get_payment(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    payment = _create_payment(db, name=name)

    stored_payment = crud.payment.get(db=db, id=payment.id)
    assert stored_payment
    _compare_entries(payment, stored_payment)


def test_get_payment_with_invalid_id_returns_none(db: Session) -> None:
    stored_payment = crud.item.get(db=db, id=-1)
    assert stored_payment is None


def test_update_payment(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    payment = _create_payment(db, name=name)

    name2 = random_string(length=randint(3, 30))
    payment_update = PaymentUpdate(name=name2)

    payment2 = crud.payment.update(db=db, db_obj=payment, obj_in=payment_update)
    _compare_entries(payment, payment2)


def test_remove_payment(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    payment = _create_payment(db, name=name)

    payment2 = crud.payment.remove(db=db, id=payment.id)
    payment3 = crud.payment.get(db=db, id=payment.id)
    assert payment3 is None
    _compare_entries(payment, payment2)


def test_remove_payment_with_invalid_id_raises_exception(db: Session) -> None:
    with pytest.raises(DBException):
        crud.payment.remove(db=db, id=-1)
