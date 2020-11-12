from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .category import Category


class Expense(Base):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    date = Column(Date)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="expenses")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="owner")

