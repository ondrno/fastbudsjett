from typing import List
from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session

from . import crud, schemas
from ..database import get_db


router = APIRouter()


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/{user_id}/", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, user_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    stored_user = schemas.UserUpdate(**db_user.__dict__)
    update_data = user.dict(exclude_unset=True)
    updated_user = stored_user.copy(update=update_data)
    print(f"*** updated data={update_data}")
    crud.update_user(db, user_id, user=updated_user)
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", response_model=schemas.UserDelete)
def delete_user_by_id(user_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
    return schemas.UserDelete(**db_user.__dict__)

