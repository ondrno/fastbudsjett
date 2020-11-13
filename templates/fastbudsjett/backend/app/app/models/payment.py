from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class PaymentMethod(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

    item_id = Column(Integer, ForeignKey("item.id"))
    item = relationship("Item", back_populates="payment_method")
