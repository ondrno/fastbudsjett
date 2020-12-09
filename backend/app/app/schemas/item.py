import datetime
import re

from typing import Optional
from pydantic import BaseModel, constr, Field, validator


# description has to have a minimum length of 10 characters
description_constr = constr(min_length=6, max_length=300)


def validate_date(v: str) -> str:
    """
    Check if the string matches either the common European date format (DD.MM.YYYY)
    or the iso format (YYYY-MM-DD)
    """
    if not isinstance(v, str):
        raise ValueError(f'Wrong argument type: {v}')

    m_regular = re.match(r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})', v)
    m_iso = re.match(r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})', v)
    if not m_regular and not m_iso:
        raise ValueError(f'Wrong date format: {v}')

    m = m_regular
    if not m:
        m = m_iso

    year = int(m.group('year'))
    month = int(m.group('month'))
    day = int(m.group('day'))
    return datetime.date(year, month, day).isoformat()


# Shared properties
class ItemBase(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = Field(None, example="9.95")
    date: Optional[str] = Field(None, example="31.12.2020")

    category_id: Optional[int] = None
    payment_id: Optional[int] = None
    itemtype_id: Optional[int] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    """
    Create an item: mandatory fields are description, amount, date, itemtype_id, category_id, payment_id
    """
    description: description_constr
    amount: float
    date: str

    category_id: int
    payment_id: int
    itemtype_id: int

    @validator("date", pre=True)
    def check_date(cls, date: str) -> str:
        return validate_date(date)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    description: Optional[description_constr]

    @validator("date", pre=True)
    def check_date(cls, date: str) -> str:
        return validate_date(date)


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    description: description_constr
    amount: float
    date: datetime.date

    owner_id: int
    category_id: int
    payment_id: int
    itemtype_id: int

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
