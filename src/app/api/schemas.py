from typing import List, Optional
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3)


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    owner_id: int
    created_date: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    notes: List[Note] = []

    class Config:
        orm_mode = True
