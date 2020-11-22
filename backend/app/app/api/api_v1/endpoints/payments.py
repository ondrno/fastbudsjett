from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sqlalchemy

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Payment])
def read_payments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve payment methods.
    """
    payments = crud.payment.get_multi(db, skip=skip, limit=limit)
    return payments


@router.post("/", response_model=schemas.Payment)
def create_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment_in: schemas.PaymentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new payment method.
    """
    try:
        payment = crud.payment.create(db=db, obj_in=payment_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="The payment with this name already exists.")

    return payment


@router.put("/{id}", response_model=schemas.Payment)
def update_payment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    payment_in: schemas.PaymentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a payment method.
    """
    payment = crud.payment.get(db=db, id=id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    try:
        payment = crud.payment.update(db=db, db_obj=payment, obj_in=payment_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="The payment with this name already exists.")
    return payment


@router.get("/{id}", response_model=schemas.Payment)
def read_payment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get payment method by ID.
    """
    payment = crud.payment.get(db=db, id=id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.delete("/{id}", response_model=schemas.Payment)
def delete_payment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a payment method. Only superusers can do that.
    """
    payment = crud.payment.get(db=db, id=id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    payment = crud.payment.remove(db=db, id=id)
    return payment
