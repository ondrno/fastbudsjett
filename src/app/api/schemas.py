from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, SecretStr


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
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None


class UserCreate(UserBase):
    email: EmailStr
    password = SecretStr


class UserUpdate(UserBase):
    pass


class UserDelete(UserBase):
    id: int


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    notes: List[Note] = []

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass
