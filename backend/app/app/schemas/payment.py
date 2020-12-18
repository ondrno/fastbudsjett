from typing import Optional
from pydantic import BaseModel, constr, PositiveInt


name_constr = constr(min_length=2, max_length=30)


# Shared properties
class PaymentBase(BaseModel):
    """
    Payment base class, the name describes the payment method, e.g. debit_card, cash, transfer
    """
    name: Optional[str] = None


# Properties to receive via API on creation
class PaymentCreate(PaymentBase):
    name: name_constr


# Properties to receive via API on update
class PaymentUpdate(PaymentBase):
    name: name_constr


class PaymentInDBBase(PaymentBase):
    id: PositiveInt
    name: name_constr

    class Config:
        orm_mode = True


# Additional properties to return via API
class Payment(PaymentInDBBase):
    pass


# Properties properties stored in DB
class PaymentInDB(PaymentInDBBase):
    pass
