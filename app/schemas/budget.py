from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class BudgetCreate(BaseModel):
    category_id: int
    month: str
    limit_amount: Decimal


class BudgetUpdate(BaseModel):
    limit_amount: Optional[Decimal] = None


class BudgetResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    month: str
    limit_amount: Decimal

    model_config = {"from_attributes": True}