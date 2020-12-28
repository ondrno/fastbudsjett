from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
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
    owner_id: Optional[int] = None,
    description: Optional[str] = None,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    start_date: Optional[str] = Query(None, regex=r'^\d{4}-\d{2}-\d{2}$'),
    end_date: Optional[str] = Query(None, regex=r'^\d{4}-\d{2}-\d{2}$'),
    category: Optional[List[int]] = Query(None),
    payment: Optional[List[int]] = Query(None),
    order_by: Optional[str] = Query(
        None,
        regex=r'^(id|description|date|created_at|modified_at|amount|owner_id|category_id|payment_id)$'
    ),
    skip: int = 0,
    limit: int = 200,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    items = crud.item.get_multi(db, owner_id=owner_id, description=description,
                                min_val=min_val, max_val=max_val,
                                start_date=start_date, end_date=end_date,
                                category=category, payment=payment,
                                skip=skip, limit=limit, order_by=order_by)
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
