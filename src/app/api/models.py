from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    notes = relationship("Note", back_populates="owner")

    @staticmethod
    def create_hashed_password(password) -> str:
        return password.get_secret_value() + "notreallyhashed"


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    description = Column(String, index=True)
    date_created = Column(DateTime, server_default=func.now(), nullable=False),
    date_updated = Column(DateTime, onupdate=func.now()),
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="notes")
