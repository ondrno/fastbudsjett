from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sqlalchemy

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


def _defined_or_http_exception_404(var, detail: str = "ItemType not found"):
    if var is None:
        raise HTTPException(status_code=404, detail=detail)


@router.get("/", response_model=List[schemas.ItemType])
def read_itemtypes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve itemtypes.
    """
    itemtypes = crud.itemtype.get_multi(db, skip=skip, limit=limit)
    return itemtypes


@router.post("/", response_model=schemas.ItemType)
def create_itemtype(
    *,
    db: Session = Depends(deps.get_db),
    itemtype_in: schemas.ItemTypeCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new itemtype.
    """
    try:
        itemtype = crud.itemtype.create(db=db, obj_in=itemtype_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="The itemtype with this title_en already exists.")

    return itemtype


@router.put("/{id}", response_model=schemas.ItemType)
def update_itemtype(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    itemtype_in: schemas.ItemTypeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a itemtype.
    """
    itemtype = crud.itemtype.get(db=db, id=id)
    _defined_or_http_exception_404(itemtype)
    try:
        itemtype = crud.itemtype.update(db=db, db_obj=itemtype, obj_in=itemtype_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="The itemtype with this title_en already exists.")
    return itemtype


@router.get("/{id}", response_model=schemas.ItemType)
def read_itemtype(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get itemtype by ID.
    """
    itemtype = crud.itemtype.get(db=db, id=id)
    _defined_or_http_exception_404(itemtype)
    return itemtype


@router.delete("/{id}", response_model=schemas.ItemType)
def delete_itemtype(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a itemtype. Only superusers can do that.
    """
    itemtype = crud.itemtype.get(db=db, id=id)
    _defined_or_http_exception_404(itemtype)
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    itemtype = crud.itemtype.remove(db=db, id=id)
    return itemtype
