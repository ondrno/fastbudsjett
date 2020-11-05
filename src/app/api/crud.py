from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()


def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_item = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# from .models import NoteSchema
# from ..database import notes, database
#
#
# async def post(payload: NoteSchema):
#     query = notes.insert().values(title=payload.title, description=payload.description)
#     return await database.execute(query=query)
#
#
# async def get(note_id: int):
#     query = notes.select().where(note_id == notes.c.id)
#     return await database.fetch_one(query=query)
#
#
# async def get_all():
#     query = notes.select()
#     return await database.fetch_all(query=query)
#
#
# async def put(id: int, payload: NoteSchema):
#     query = (
#         notes
#         .update()
#         .where(id == notes.c.id)
#         .values(title=payload.title, description=payload.description)
#         .returning(notes.c.id)
#     )
#     return await database.execute(query=query)
#
#
# async def delete(id: int):
#     query = notes.delete().where(id == notes.c.id)
#     return await database.execute(query=query)
