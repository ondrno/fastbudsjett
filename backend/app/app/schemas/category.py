from typing import Optional
from pydantic import BaseModel, constr


name_constr = constr(min_length=3, max_length=30)


# Shared properties
class CategoryBase(BaseModel):
    name: Optional[str] = None
    itemtype_id: Optional[int] = None


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    name: name_constr
    itemtype_id: int


# Properties to receive on category update
class CategoryUpdate(CategoryBase):
    name: Optional[str] = name_constr
    itemtype_id: Optional[int]


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int
    name: name_constr
    itemtype_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
