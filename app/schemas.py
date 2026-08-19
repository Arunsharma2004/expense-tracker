from datetime import date as date_type

from pydantic import BaseModel, ConfigDict, Field

from app.models import Category


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: Category
    date: date_type


class ExpenseUpdate(BaseModel):
    amount: float = Field(gt=0)
    category: Category
    date: date_type


class ExpenseOut(ExpenseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BudgetCreate(BaseModel):
    category: Category
    amount: float = Field(gt=0)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=1)


class BudgetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: Category
    amount: float
    month: int
    year: int
