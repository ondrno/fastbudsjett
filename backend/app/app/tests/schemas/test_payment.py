from fastapi.exceptions import ValidationError
from sqlalchemy.orm import Session
import pytest

from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.tests.utils.utils import random_string


def test_create_payment_too_long_name_raises_exception(db: Session) -> None:
    name = random_string(length=31)
    with pytest.raises(ValidationError):
        PaymentCreate(name=name)


def test_create_payment_too_short_name_raises_exception(db: Session) -> None:
    name = random_string(length=1)
    with pytest.raises(ValidationError):
        PaymentCreate(name=name)


def test_update_payment_too_long_name_raises_exception(db: Session) -> None:
    name = random_string(length=31)
    with pytest.raises(ValidationError):
        PaymentUpdate(name=name)


def test_update_payment_too_short_name_raises_exception(db: Session) -> None:
    name = random_string(length=1)
    with pytest.raises(ValidationError):
        PaymentUpdate(name=name)


def test_update_payment_with_no_data_raises_exception(db: Session) -> None:
    with pytest.raises(ValidationError):
        PaymentUpdate()
