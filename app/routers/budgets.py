from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from app.services.budget_service import (
    get_budgets,
    get_budget,
    create_budget,
    update_budget,
    delete_budget
)
from app.dependencies.auth import get_db, get_current_user
from app.models.user import User


router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("/", response_model=list[BudgetResponse])
def list_budgets(
    month: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_budgets(db, current_user.id, month)


@router.post("/", response_model=BudgetResponse)
def create(
    data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_budget(db, current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_one(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budget = get_budget(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.put("/{budget_id}", response_model=BudgetResponse)
def update(
    budget_id: int,
    data: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budget = update_budget(db, budget_id, current_user.id, data)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.delete("/{budget_id}")
def delete(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = delete_budget(db, budget_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"message": "Budget deleted"}