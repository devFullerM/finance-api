from sqlalchemy.orm import Session
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate
from typing import Optional


def get_budgets(db: Session, user_id: int, month: Optional[str] = None) -> list[Budget]:
    query = db.query(Budget).filter(Budget.user_id == user_id)
    if month:
        query = query.filter(Budget.month == month)
    return query.all()


def get_budget(db: Session, budget_id: int, user_id: int) -> Budget | None:
    return db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == user_id
    ).first()


def create_budget(db: Session, user_id: int, data: BudgetCreate) -> Budget:
    existing = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category_id == data.category_id,
        Budget.month == data.month
    ).first()
    if existing:
        raise ValueError("Budget already exists for this category and month")

    budget = Budget(
        user_id=user_id,
        category_id=data.category_id,
        month=data.month,
        limit_amount=data.limit_amount
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def update_budget(db: Session, budget_id: int, user_id: int, data: BudgetUpdate) -> Budget | None:
    budget = get_budget(db, budget_id, user_id)
    if not budget:
        return None
    if data.limit_amount is not None:
        budget.limit_amount = data.limit_amount
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, budget_id: int, user_id: int) -> bool:
    budget = get_budget(db, budget_id, user_id)
    if not budget:
        return False
    db.delete(budget)
    db.commit()
    return True