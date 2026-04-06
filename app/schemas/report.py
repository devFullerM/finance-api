from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class MonthlySummary(BaseModel):
    month: str
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal


class CategorySpend(BaseModel):
    category_id: int
    category_name: str
    total_spent: Decimal
    budget_limit: Optional[Decimal] = None
    remaining: Optional[Decimal] = None
    is_over_budget: Optional[bool] = None