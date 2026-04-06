from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    colour: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    colour: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str
    colour: Optional[str] = None

    model_config = {"from_attributes": True}