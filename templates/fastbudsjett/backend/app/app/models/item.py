from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .category import Category  # noqa: F401
    from .payment import PaymentMethod  # noqa: F401


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(250), index=True)
    amount = Column(Integer)
    date = Column(Date)
    is_deleted = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="owner")

    payment_method_id = Column(Integer, ForeignKey("paymentMethod.id"))
    payment_method = relationship("PaymentMethod", back_populates="item")
    _date_created = Column(Date)
    _date_modified = Column(Date)
