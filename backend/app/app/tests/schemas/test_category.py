from fastapi.exceptions import ValidationError
from sqlalchemy.orm import Session
import pytest

from app.schemas.category import CategoryCreate, CategoryUpdate
from app.tests.utils.utils import random_string


def test_create_category_too_long_name_raises_exception(db: Session) -> None:
    name = random_string(length=40)
    with pytest.raises(ValidationError):
        CategoryCreate(name=name)


def test_create_category_too_short_name_raises_exception(db: Session) -> None:
    name = random_string(length=2)
    with pytest.raises(ValidationError):
        CategoryCreate(name=name)


def test_update_category_too_long_name_raises_exception(db: Session) -> None:
    name = random_string(length=40)
    with pytest.raises(ValidationError):
        CategoryUpdate(name=name)


def test_update_category_too_short_name_raises_exception(db: Session) -> None:
    name = random_string(length=2)
    with pytest.raises(ValidationError):
        CategoryUpdate(name=name)


def test_update_category_with_no_data_raises_exception(db: Session) -> None:
    with pytest.raises(ValidationError):
        CategoryUpdate()
