from typing import Optional
from pydantic import BaseModel, PositiveInt, constr, root_validator


name_constr = constr(min_length=3, max_length=30)


# Shared properties
class CategoryBase(BaseModel):
    title_en: Optional[str] = None
    title_de: Optional[str] = None
    itemtype_id: Optional[PositiveInt] = None


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    title_en: name_constr
    title_de: name_constr
    itemtype_id: PositiveInt


# Properties to receive on category update
class CategoryUpdate(CategoryBase):
    title_en: Optional[name_constr]
    title_de: Optional[name_constr]
    itemtype_id: Optional[PositiveInt]

    @root_validator(pre=True)
    def check_any_of(cls, values):
        if not values.keys():
            raise ValueError("Either 'title_en', 'title_de' or 'itemtype_id' has to be given")
        else:
            return values


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: PositiveInt
    title_en: name_constr
    title_de: name_constr
    itemtype_id: PositiveInt

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
