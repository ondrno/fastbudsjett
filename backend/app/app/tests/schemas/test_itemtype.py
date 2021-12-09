from fastapi.exceptions import ValidationError
from sqlalchemy.orm import Session
import pytest

from app.schemas.itemtype import ItemTypeCreate, ItemTypeUpdate
from app.tests.utils.utils import random_string


def test_create_itemtype_too_long_name_raises_exception(db: Session) -> None:
    name = random_string(length=40)
    with pytest.raises(ValidationError):
        ItemTypeCreate(name=name)


def test_create_itemtype_too_short_name_raises_exception(db: Session) -> None:
    name = random_string(length=2)
    with pytest.raises(ValidationError):
        ItemTypeCreate(name=name)


def test_update_itemtype_too_long_name_raises_exception(db: Session) -> None:
    name = random_string(length=40)
    with pytest.raises(ValidationError):
        ItemTypeUpdate(name=name)


def test_update_itemtype_too_short_name_raises_exception(db: Session) -> None:
    name = random_string(length=2)
    with pytest.raises(ValidationError):
        ItemTypeUpdate(name=name)


def test_update_itemtype_with_no_data_raises_exception(db: Session) -> None:
    with pytest.raises(ValidationError):
        ItemTypeUpdate()
