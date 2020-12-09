from typing import Optional
from pydantic import BaseModel, constr


name_constr = constr(min_length=2, max_length=30)


# Shared properties
class ItemTypeBase(BaseModel):
    """
    ItemType base class, the name describes the item type, i.e. revenue or expenditures
    """
    name: Optional[str] = None


# Properties to receive via API on creation
class ItemTypeCreate(ItemTypeBase):
    name: name_constr


# Properties to receive via API on update
class ItemTypeUpdate(ItemTypeBase):
    name: name_constr


class ItemTypeInDBBase(ItemTypeBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class ItemType(ItemTypeInDBBase):
    pass


# Properties properties stored in DB
class ItemTypeInDB(ItemTypeInDBBase):
    pass
