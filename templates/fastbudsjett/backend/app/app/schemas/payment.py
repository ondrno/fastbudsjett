from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class PaymentMethodBase(BaseModel):
    title: Optional[str] = None


# Properties to receive via API on creation
class PaymentMethodCreate(PaymentMethodBase):
    title: str


# Properties to receive via API on update
class PaymentMethodUpdate(PaymentMethodBase):
    title: Optional[str] = None


class PaymentMethodInDBBase(PaymentMethodBase):
    id: int
    title: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class PaymentMethod(PaymentMethodInDBBase):
    pass
