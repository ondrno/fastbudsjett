from typing import Optional
from pydantic import BaseModel, PositiveInt, constr, root_validator


name_constr = constr(min_length=3, max_length=30)


# Shared properties
class CategoryBase(BaseModel):
    name: Optional[str] = None
    itemtype_id: Optional[PositiveInt] = None


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    name: name_constr
    itemtype_id: PositiveInt


# Properties to receive on category update
class CategoryUpdate(CategoryBase):
    name: Optional[name_constr]
    itemtype_id: Optional[PositiveInt]

    @root_validator(pre=True)
    def check_any_of(cls, values):
        if not values.keys():
            raise ValueError("Either 'name' or 'itemtype_id' has to be given")
        else:
            return values


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: PositiveInt
    name: name_constr
    itemtype_id: PositiveInt

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
