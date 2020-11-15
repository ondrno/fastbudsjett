from typing import Optional
from datetime import datetime
from pydantic import BaseModel, constr, Field


# description has to have a minimum length of 10 characters
description_constr = constr(min_length=10, max_length=300)

# only accept date strings such dd.mm.yyyy, e.g. 05.12.2020
date_constr = constr(min_length=10, max_length=10, regex=r'\d{2}\.\d{2}\.\d{4}')


# Shared properties
class ItemBase(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = Field(None, example="9.95")
    date: Optional[str] = Field(None, example="01.12.2020")

    category_id: Optional[int] = None
    payment_id: Optional[int] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    description: description_constr
    amount: float
    date: date_constr

    category_id: int
    payment_id: int


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    description: description_constr
    amount: float
    date: date_constr

    owner_id: int
    category_id: int
    payment_id: int

    _date_created: datetime
    _date_modified: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
