from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


NOT_ENOUGH_PERMISSIONS = "Not enough permissions"
ITEM_NOT_FOUND = "Item not found"


def _defined_or_http_exception_404(var, detail: str = ITEM_NOT_FOUND) -> None:
    if var is None:
        raise HTTPException(status_code=404, detail=detail)


def _superuser_or_owner_or_http_exception_400(current_user, owner_id: int) -> None:
    if not crud.user.is_superuser(current_user) and (owner_id != current_user.id):
        raise HTTPException(status_code=400, detail=NOT_ENOUGH_PERMISSIONS)


router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.put("/{id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = crud.item.get(db=db, id=id)
    _defined_or_http_exception_404(item)
    _superuser_or_owner_or_http_exception_400(current_user, item.owner_id)
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.item.get(db=db, id=id)
    _defined_or_http_exception_404(item)
    _superuser_or_owner_or_http_exception_400(current_user, item.owner_id)
    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.item.get(db=db, id=id)
    _defined_or_http_exception_404(item)
    _superuser_or_owner_or_http_exception_400(current_user, item.owner_id)
    item = crud.item.remove(db=db, id=id)
    return item
