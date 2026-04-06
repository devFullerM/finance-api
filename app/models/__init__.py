# Alembic migration tool will automatically detect all models in this package
# Importing them all here means we can point Alembic at app.models and it will find everything automatically.
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.budget import Budget