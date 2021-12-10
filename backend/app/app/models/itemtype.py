from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401
    from .category import Category  # noqa: F401


class ItemType(Base):
    """
    ItemType class, it differentiates between revenues and expenditures
    """
    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String, index=True, nullable=True)
    title_de = Column(String, index=True, nullable=True)
    items = relationship("Item", back_populates="itemtype")
    category = relationship("Category", back_populates="itemtype")
