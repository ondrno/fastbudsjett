from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    pass


payment = CRUDPayment(Payment)
