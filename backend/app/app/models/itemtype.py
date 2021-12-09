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
    name = Column(String, index=True, unique=True, nullable=False)
    items = relationship("Item", back_populates="itemtype")
    category = relationship("Category", back_populates="itemtype")
