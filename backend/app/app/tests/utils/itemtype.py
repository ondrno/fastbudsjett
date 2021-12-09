from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.itemtype import ItemTypeCreate
from app.tests.utils.utils import random_string


def create_random_itemtype(db: Session) -> models.ItemType:
    name = random_string(length=5)
    itemtype_in = ItemTypeCreate(name=name)
    return crud.itemtype.create(db=db, obj_in=itemtype_in)
