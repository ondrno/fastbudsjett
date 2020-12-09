from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401
    from .itemtype import ItemType  # noqa: F401


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True, unique=True, nullable=False)
    items = relationship("Item", back_populates="category")

    itemtype_id = Column(Integer, ForeignKey("itemtype.id"), nullable=False)
    itemtype = relationship("ItemType", back_populates="category")
