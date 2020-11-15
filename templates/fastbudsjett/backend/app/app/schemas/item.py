import datetime
import re

from typing import Optional
from pydantic import BaseModel, constr, Field, validator


# description has to have a minimum length of 10 characters
description_constr = constr(min_length=10, max_length=300)


def validate_date(v: str) -> str:
    if not isinstance(v, str):
        raise ValueError(f'Wrong argument type: {v}')

    m = re.match(r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})', v)
    if not m:
        raise ValueError(f'Wrong date format: {v}')

    year = int(m.group('year'))
    month = int(m.group('month'))
    day = int(m.group('day'))
    return datetime.date(year, month, day).isoformat()


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
    date: str

    category_id: int
    payment_id: int

    @validator("date", pre=True)
    def check_date(cls, date: str) -> str:
        return validate_date(date)


# Properties to receive on item update
class ItemUpdate(ItemBase):

    @validator("date", pre=True)
    def check_date(cls, date: str) -> str:
        return validate_date(date)


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    description: description_constr
    amount: float
    date: str

    owner_id: int
    category_id: int
    payment_id: int

    _date_created: datetime.datetime
    _date_modified: datetime.datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
