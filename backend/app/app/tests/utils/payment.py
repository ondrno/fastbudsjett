from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.payment import PaymentCreate
from app.tests.utils.utils import random_lower_string


def create_random_payment(db: Session) -> models.Payment:
    name = random_lower_string()
    payment_in = PaymentCreate(name=name)
    return crud.payment.create(db=db, obj_in=payment_in)
