from typing import Optional
from pydantic import BaseModel, constr


name_constr = constr(min_length=3, max_length=30)


# Shared properties
class ItemTypeBase(BaseModel):
    """
    ItemType base class, the title_en describes the item type, i.e. income or expense
    """
    title_en: Optional[str] = None
    title_de: Optional[str] = None


# Properties to receive via API on creation
class ItemTypeCreate(ItemTypeBase):
    title_en: name_constr
    title_de: name_constr


# Properties to receive via API on update
class ItemTypeUpdate(ItemTypeBase):
    title_en: name_constr
    title_de: name_constr


class ItemTypeInDBBase(ItemTypeBase):
    id: int
    title_en: name_constr
    title_de: name_constr

    class Config:
        orm_mode = True


# Additional properties to return via API
class ItemType(ItemTypeInDBBase):
    pass


# Properties properties stored in DB
class ItemTypeInDB(ItemTypeInDBBase):
    pass
