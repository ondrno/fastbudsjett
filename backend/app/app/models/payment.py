from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class Payment(Base):
    """
    Payment class contains the different methods to pay, e.g.
    debit card, cash, bank transfer
    """
    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String, index=True, nullable=True)
    title_de = Column(String, index=True, nullable=True)
    items = relationship("Item", back_populates="payment")
