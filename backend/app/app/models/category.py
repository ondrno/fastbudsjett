from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401
    from .itemtype import ItemType  # noqa: F401


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, nullable=True, index=True)
    title_en = Column(String(30), index=True, nullable=True)
    title_de = Column(String(30), index=True, nullable=True)
    items = relationship("Item", back_populates="category")

    itemtype_id = Column(Integer, ForeignKey("itemtype.id"), nullable=False)
    itemtype = relationship("ItemType", back_populates="category")
