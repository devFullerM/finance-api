from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.report import MonthlySummary, CategorySpend
from app.services.report_service import get_monthly_summary, get_spending_by_category
from app.dependencies.auth import get_db, get_current_user
from app.models.user import User


router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly-summary", response_model=MonthlySummary)
def monthly_summary(
    month: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_monthly_summary(db, current_user.id, month)


@router.get("/by-category", response_model=list[CategorySpend])
def by_category(
    month: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_spending_by_category(db, current_user.id, month)