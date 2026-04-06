from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class TransactionCreate(BaseModel):
    category_id: int
    amount: float
    type: TransactionType
    description: Optional[str] = None
    transaction_date: datetime


class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    description: Optional[str] = None
    transaction_date: Optional[datetime] = None


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: float
    type: TransactionType
    description: Optional[str] = None
    transaction_date: datetime
    created_at: datetime

    model_config = {"from_attributes": True}