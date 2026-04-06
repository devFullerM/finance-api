from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from calendar import monthrange
from app.models.transaction import Transaction, TransactionType
from app.models.budget import Budget
from app.models.category import Category
from app.schemas.report import MonthlySummary, CategorySpend


def get_monthly_summary(db: Session, user_id: int, month: str) -> MonthlySummary:
    year, mon = map(int, month.split("-"))
    last_day = monthrange(year, mon)[1]
    start = f"{month}-01"
    end = f"{month}-{last_day:02d}"

    results = db.query(
        Transaction.type,
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_date >= start,
        Transaction.transaction_date <= end
    ).group_by(Transaction.type).all()

    total_income = Decimal("0")
    total_expenses = Decimal("0")

    for row in results:
        if row.type == TransactionType.income:
            total_income = Decimal(str(row.total))
        elif row.type == TransactionType.expense:
            total_expenses = Decimal(str(row.total))

    return MonthlySummary(
        month=month,
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=total_income - total_expenses
    )


def get_spending_by_category(db: Session, user_id: int, month: str) -> list[CategorySpend]:
    year, mon = map(int, month.split("-"))
    last_day = monthrange(year, mon)[1]
    start = f"{month}-01"
    end = f"{month}-{last_day:02d}"

    results = db.query(
        Category.id,
        Category.name,
        func.sum(Transaction.amount).label("total_spent")
    ).join(
        Transaction, Transaction.category_id == Category.id
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == TransactionType.expense,
        Transaction.transaction_date >= start,
        Transaction.transaction_date <= end
    ).group_by(Category.id, Category.name).all()

    spending = []

    for row in results:
        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category_id == row.id,
            Budget.month == month
        ).first()

        total_spent = Decimal(str(row.total_spent))
        budget_limit = Decimal(str(budget.limit_amount)) if budget else None
        remaining = (budget_limit - total_spent) if budget_limit is not None else None
        is_over_budget = (total_spent > budget_limit) if budget_limit is not None else None

        spending.append(CategorySpend(
            category_id=row.id,
            category_name=row.name,
            total_spent=total_spent,
            budget_limit=budget_limit,
            remaining=remaining,
            is_over_budget=is_over_budget
        ))

    return spending