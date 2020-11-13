from typing import Optional

from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    description: Optional[str] = None
    amount: Optional[int] = None
    date: Optional[str] = None
    is_deleted: Optional[bool] = None
    category_id: Optional[int] = None
    payment_method_id: Optional[int] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    description: str
    amount: int
    date: str
    category_id: int
    payment_method_id: int


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    description: str
    amount: int
    is_deleted: bool = False
    date_created: str
    date_modified: str
    owner_id: int
    category_id: int
    payment_method_id: int
    _date_created: str
    _date_modified: str

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
