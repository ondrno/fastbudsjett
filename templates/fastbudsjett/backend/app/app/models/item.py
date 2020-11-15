from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Float, Date, DateTime, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .category import Category  # noqa: F401
    from .payment import Payment  # noqa: F401


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(300), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="items")

    payment_id = Column(Integer, ForeignKey("payment.id"))
    payment = relationship("Payment", back_populates="items")

    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    removed_at = Column(DateTime, nullable=True)
