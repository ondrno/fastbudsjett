from typing import Optional
from pydantic import BaseModel, constr


name_constr = constr(min_length=3, max_length=30)


# Shared properties
class CategoryBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on item creation
class CategoryCreate(CategoryBase):
    name: name_constr


# Properties to receive on item update
class CategoryUpdate(CategoryBase):
    name: name_constr


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int
    name: name_constr

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
