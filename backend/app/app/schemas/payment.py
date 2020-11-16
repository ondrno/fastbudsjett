from typing import Optional
from pydantic import BaseModel


# Shared properties
class PaymentBase(BaseModel):
    """
    Payment base class, the name describes the payment method, e.g. debit_card, cash, transfer
    """
    name: Optional[str] = None


# Properties to receive via API on creation
class PaymentCreate(PaymentBase):
    name: str


# Properties to receive via API on update
class PaymentUpdate(PaymentBase):
    name: Optional[str] = None


class PaymentInDBBase(PaymentBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Payment(PaymentInDBBase):
    pass


# Properties properties stored in DB
class PaymentInDB(PaymentInDBBase):
    pass
