from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import (
    get_categories,
    get_category,
    create_category,
    update_category,
    delete_category
)
from app.dependencies.auth import get_db, get_current_user
from app.models.user import User


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_categories(db, current_user.id)


@router.post("/", response_model=CategoryResponse)
def create(data: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_category(db, current_user.id, data)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_one(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = get_category(db, category_id, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = update_category(db, category_id, current_user.id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = delete_category(db, category_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}