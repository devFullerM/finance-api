from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_categories(db: Session, user_id: int) -> list[Category]:
    return db.query(Category).filter(Category.user_id == user_id).all()


def get_category(db: Session, category_id: int, user_id: int) -> Category | None:
    return db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()


def create_category(db: Session, user_id: int, data: CategoryCreate) -> Category:
    category = Category(
        user_id=user_id,
        name=data.name,
        colour=data.colour
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, user_id: int, data: CategoryUpdate) -> Category | None:
    category = get_category(db, category_id, user_id)
    if not category:
        return None
    if data.name is not None:
        category.name = data.name
    if data.colour is not None:
        category.colour = data.colour
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int, user_id: int) -> bool:
    category = get_category(db, category_id, user_id)
    if not category:
        return False
    db.delete(category)
    db.commit()
    return True