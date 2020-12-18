from sqlalchemy.orm import Session
import pytest
from random import randint

from app import crud
from app.db.exc import DBException
from app.schemas.itemtype import ItemTypeCreate, ItemTypeUpdate
from app.schemas.item import ItemCreate
from app.schemas.category import CategoryCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_string


def _create_schema_for_itemtype(name: str) -> ItemTypeCreate:
    return ItemTypeCreate(name=name)


def _create_itemtype(db: Session, name: str):
    itemtype_in = _create_schema_for_itemtype(name)
    return crud.itemtype.create(db=db, obj_in=itemtype_in)


def _compare_entries(a, b):
    assert a.name == b.name
    assert a.id == b.id
    assert a.items == b.items
    assert a.category == b.category


def test_create_itemtype(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = _create_itemtype(db, name=name)
    assert itemtype.name == name
    assert itemtype.items == []
    assert itemtype.category == []


def test_itemtype_items_field_is_propagated_by_category_and_items(db: Session, test_payment) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = _create_itemtype(db, name=name)
    assert itemtype.name == name
    assert itemtype.items == []
    assert itemtype.category == []

    category_in = CategoryCreate(name=name, itemtype_id=itemtype.id)
    category = crud.category.create(db=db, obj_in=category_in)

    user = create_random_user(db)
    item_in = ItemCreate(description="test_description", amount="12.20", date="01.01.2020",
                         category_id=category.id, payment_id=test_payment.id, itemtype_id=itemtype.id)
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user.id)
    assert itemtype.items == [item]
    assert itemtype.category == [category]

    crud.item.remove(db=db, id=item.id)
    assert itemtype.items == []


def test_get_itemtype(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = _create_itemtype(db, name=name)

    stored_itemtype = crud.itemtype.get(db=db, id=itemtype.id)
    assert stored_itemtype
    _compare_entries(itemtype, stored_itemtype)


def test_get_itemtype_with_invalid_id_returns_none(db: Session) -> None:
    stored_itemtype = crud.item.get(db=db, id=-1)
    assert stored_itemtype is None


def test_update_itemtype(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = _create_itemtype(db, name=name)

    name2 = random_string(length=randint(3, 30))
    itemtype_update = ItemTypeUpdate(name=name2)

    itemtype2 = crud.itemtype.update(db=db, db_obj=itemtype, obj_in=itemtype_update)
    _compare_entries(itemtype, itemtype2)


def test_remove_itemtype(db: Session, test_itemtype, test_payment) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = _create_itemtype(db, name=name)

    itemtype2 = crud.itemtype.remove(db=db, id=itemtype.id)
    itemtype3 = crud.itemtype.get(db=db, id=itemtype.id)
    assert itemtype3 is None
    _compare_entries(itemtype, itemtype2)


def test_remove_itemtype_with_invalid_id_raises_exception(db: Session) -> None:
    with pytest.raises(DBException):
        crud.itemtype.remove(db=db, id=-1)
