from sqlalchemy.orm import Session
import mock
import pytest
from random import randint

from app import crud
from app.db.exc import DBException
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.item import ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_string


def _create_schema_for_category(name: str, itemtype_id: int) -> CategoryCreate:
    return CategoryCreate(name=name, itemtype_id=itemtype_id)


def _create_category(db: Session, name: str, itemtype_id: int):
    category_in = _create_schema_for_category(name, itemtype_id)
    return crud.category.create(db=db, obj_in=category_in)


def _compare_entries(a, b):
    assert a.name == b.name
    assert a.itemtype_id == b.itemtype_id
    assert a.id == b.id
    assert a.items == b.items


def test_create_category(db: Session, test_itemtype) -> None:
    name = random_string(length=randint(3, 30))
    category = _create_category(db, name=name, itemtype_id=test_itemtype.id)
    assert category.name == name
    assert category.itemtype_id == test_itemtype.id
    assert category.items == []


def test_category_items_field_is_propagated_by_items(db: Session, test_payment) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = mock.MagicMock()
    category = _create_category(db, name=name, itemtype_id=itemtype.id)
    assert category.name == name
    assert category.items == []

    user = create_random_user(db)
    item_in = ItemCreate(description="test_description", amount="12.20", date="01.01.2020",
                         category_id=category.id, payment_id=test_payment.id, itemtype_id=itemtype.id)
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user.id)
    assert category.items == [item]

    crud.item.remove(db=db, id=item.id)
    assert category.items == []


def test_get_category(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = mock.MagicMock()
    category = _create_category(db, name=name, itemtype_id=itemtype.id)

    stored_category = crud.category.get(db=db, id=category.id)
    assert stored_category
    _compare_entries(category, stored_category)


def test_get_category_with_invalid_id_returns_none(db: Session) -> None:
    stored_category = crud.item.get(db=db, id=-1)
    assert stored_category is None


def test_update_category(db: Session) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = mock.MagicMock()
    category = _create_category(db, name=name, itemtype_id=itemtype.id)

    name2 = random_string(length=randint(3, 30))
    category_update = CategoryUpdate(name=name2)

    category2 = crud.category.update(db=db, db_obj=category, obj_in=category_update)
    _compare_entries(category, category2)


def test_remove_category(db: Session, test_category, test_payment) -> None:
    name = random_string(length=randint(3, 30))
    itemtype = mock.MagicMock()
    category = _create_category(db, name=name, itemtype_id=itemtype.id)

    category2 = crud.category.remove(db=db, id=category.id)
    category3 = crud.category.get(db=db, id=category.id)
    assert category3 is None
    _compare_entries(category, category2)


def test_remove_category_with_invalid_id_raises_exception(db: Session) -> None:
    with pytest.raises(DBException):
        crud.category.remove(db=db, id=-1)
