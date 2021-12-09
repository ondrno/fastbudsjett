from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.category import CategoryCreate
from app.tests.utils.utils import random_string


def create_random_category(db: Session, itemtype) -> models.Category:
    name = random_string(length=30)
    category_in = CategoryCreate(name=name, itemtype_id=itemtype.id)
    return crud.category.create(db=db, obj_in=category_in)
