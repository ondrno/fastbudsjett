from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.payment import PaymentModel
from app.schemas.payment import PaymentMethodCreate, PaymentMethodUpdate


class CRUDPaymentMethod(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass


payment_method = CRUDPaymentMethod(PaymentModel)
