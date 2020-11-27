from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import sqlalchemy

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.db.exc import DBException


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except sqlalchemy.exc.IntegrityError as e:
            raise DBException(f"Database integrity error = {e}")
        return db_obj

    def get_multi(
        self, db: Session, *,
            skip: int = 0, limit: int = 100,
            owner_id: Optional[int] = None,
            description: Optional[str] = None,
            min_val: Optional[float] = None,
            max_val: Optional[float] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            category: Optional[List[int]] = None,
            payment: Optional[List[int]] = None,
    ) -> List[Item]:
        filter_expr = None
        if description:
            filter_expr = f"Item.description like '%{description}%'"
        if owner_id:
            if filter_expr:
                filter_expr += ","
            filter_expr = f"Item.owner_id == {owner_id}'"
        if min_val:
            if filter_expr:
                filter_expr += ","
            filter_expr = f"Item.amount >= '{min_val}'"
        if max_val:
            if filter_expr:
                filter_expr += ","
            filter_expr = f"Item.amount <= '{max_val}'"
        if start_date:
            if filter_expr:
                filter_expr += ","
            filter_expr = f"Item.date >= '{start_date}'"
        if end_date:
            if filter_expr:
                filter_expr += ","
            filter_expr = f"Item.date <= '{end_date}'"
        if category:
            if filter_expr:
                filter_expr += ","
            q = ','.join([str(x) for x in category])
            filter_expr = f"item.category_id in '({q})'"
        if payment:
            if filter_expr:
                filter_expr += ","
            q = ','.join([str(x) for x in payment])
            filter_expr = f"item.payment_id in '({q})'"

        return (
            db.query(self.model)
            .filter(filter_expr)
            .offset(skip)
            .limit(limit)
            .all()
        )


item = CRUDItem(Item)
