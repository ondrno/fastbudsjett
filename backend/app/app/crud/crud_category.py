from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_multi(
        self, db: Session, *,
            skip: int = 0, limit: int = 200,
            itemtype_id: Optional[List[int]] = None,
            parent_id: Optional[int] = None,
            order_by: str = 'itemtype_id',
    ) -> List[Category]:
        print(f"Category: locals={locals()}")
        filter_expr = ''
        if parent_id:
            filter_expr += f"Category.parent_id == {parent_id}"
        if itemtype_id:
            if filter_expr:
                filter_expr += " AND "
            q = ','.join([str(x) for x in itemtype_id])
            filter_expr += f"Category.itemtype_id in ({q})"
        filter_expr = text(filter_expr)

        order_expr = 'Category.itemtype_id'
        if order_by in ['id', 'title_en', 'title_de', 'created_at', 'modified_at', 'itemtype_id', 'parent_id']:
            order_expr = f"Category.{order_by} asc"
        order_expr = text(order_expr)
        print(f"Category: get_multi filter_expr={filter_expr} skip={skip} limit={limit}")
        return (
            db.query(self.model)
            .filter(filter_expr)
            .order_by(order_expr)
            .offset(skip)
            .limit(limit)
            .all()
        )


category = CRUDCategory(Category)
