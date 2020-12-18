from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.item import ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_string, random_float, random_date


def create_random_item(db: Session, itemtype_id: int, category_id: int, payment_id: int) -> models.Item:
    user = create_random_user(db)
    owner_id = user.id
    description = random_string()
    amount = random_float()
    date = random_date()
    item_in = ItemCreate(description=description, amount=amount, date=date, itemtype_id=itemtype_id,
                         category_id=category_id, payment_id=payment_id)
    return crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=owner_id)
