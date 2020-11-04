from app.api.models import NoteSchema
from app.db import notes, database


async def post(payload: NoteSchema):
    query = notes.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)


async def get(note_id: int):
    query = notes.select().where(note_id == notes.c.id)
    return await database.fetch_one(query=query)
