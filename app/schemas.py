from datetime import date as date_type

from pydantic import BaseModel, ConfigDict, Field

from app.models import Category


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: Category
    date: date_type


class ExpenseOut(ExpenseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
