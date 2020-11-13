from typing import Optional

from pydantic import BaseModel, datetime


# Shared properties
class ItemBase(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    is_deleted: Optional[bool] = None

    category_id: Optional[int] = None
    payment_method_id: Optional[int] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    description: str
    amount: float
    date: datetime.date

    category_id: int
    payment_method_id: int


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    description: str
    amount: float
    date: datetime.date
    is_deleted: bool = False

    owner_id: int
    category_id: int
    payment_method_id: int

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
