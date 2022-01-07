from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import sqlalchemy

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


def _defined_or_http_exception_404(var, detail: str = "Category not found"):
    if var is None:
        raise HTTPException(status_code=404, detail=detail)


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    itemtype_id: Optional[List[int]] = Query(None),
    parent_id: Optional[int] = None,
    order_by: Optional[str] = Query(
        None,
        regex=r'^(id|parent_id|itemtype_id|title_en|title_de|created_at|modified_at)$'
    ),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve categories.
    """
    categories = crud.category.get_multi(db,
                                         skip=skip, limit=limit, itemtype_id=itemtype_id,
                                         parent_id=parent_id, order_by=order_by)
    return categories


@router.post("/", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new category.
    """
    try:
        category = crud.category.create(db=db, obj_in=category_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="The category with this title_en already exists.")

    return category


@router.put("/{id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    category_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a category.
    """
    category = crud.category.get(db=db, id=id)
    _defined_or_http_exception_404(category)
    try:
        category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="The category with this title_en already exists.")
    return category


@router.get("/{id}", response_model=schemas.Category)
def read_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get category by ID.
    """
    category = crud.category.get(db=db, id=id)
    _defined_or_http_exception_404(category)
    return category


@router.delete("/{id}", response_model=schemas.Category)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a category. Only superusers can do that.
    """
    category = crud.category.get(db=db, id=id)
    _defined_or_http_exception_404(category)
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    category = crud.category.remove(db=db, id=id)
    return category
