from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from datetime import datetime
from typing import Optional


def get_transactions(
    db: Session,
    user_id: int,
    category_id: Optional[int] = None,
    type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> list[Transaction]:
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if type:
        query = query.filter(Transaction.type == type)
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    return query.all()


def get_transaction(db: Session, transaction_id: int, user_id: int) -> Transaction | None:
    return db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id
    ).first()


def create_transaction(db: Session, user_id: int, data: TransactionCreate) -> Transaction:
    transaction = Transaction(
        user_id=user_id,
        category_id=data.category_id,
        amount=data.amount,
        type=data.type,
        description=data.description,
        transaction_date=data.transaction_date
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def update_transaction(db: Session, transaction_id: int, user_id: int, data: TransactionUpdate) -> Transaction | None:
    transaction = get_transaction(db, transaction_id, user_id)
    if not transaction:
        return None
    if data.category_id is not None:
        transaction.category_id = data.category_id
    if data.amount is not None:
        transaction.amount = data.amount
    if data.type is not None:
        transaction.type = data.type
    if data.description is not None:
        transaction.description = data.description
    if data.transaction_date is not None:
        transaction.transaction_date = data.transaction_date
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    transaction = get_transaction(db, transaction_id, user_id)
    if not transaction:
        return False
    db.delete(transaction)
    db.commit()
    return True