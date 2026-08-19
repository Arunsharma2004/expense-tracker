from calendar import monthrange
from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Budget, Category, Expense
from app.schemas import (
    BudgetCreate,
    BudgetOut,
    BudgetStatus,
    ExpenseCreate,
    ExpenseOut,
    ExpenseUpdate,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker")


@app.post("/expenses", response_model=ExpenseOut, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses", response_model=list[ExpenseOut])
def list_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


@app.post("/budgets", response_model=BudgetOut, status_code=201)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    db_budget = Budget(**budget.model_dump())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


@app.get("/budgets", response_model=BudgetStatus)
def check_budget(
    category: Category,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    budget = (
        db.query(Budget)
        .filter(Budget.category == category, Budget.month == month, Budget.year == year)
        .first()
    )
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    start_date = date(year, month, 1)
    end_date = date(year, month, monthrange(year, month)[1])
    spent = (
        db.query(func.sum(Expense.amount))
        .filter(
            Expense.category == category,
            Expense.date >= start_date,
            Expense.date <= end_date,
        )
        .scalar()
        or 0
    )

    return {
        "category": category,
        "month": month,
        "year": year,
        "spent": spent,
        "remaining": budget.amount - spent,
    }


@app.get("/summary", response_model=dict[Category, float])
def get_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    start_date = date(year, month, 1)
    end_date = date(year, month, monthrange(year, month)[1])
    results = (
        db.query(Expense.category, func.sum(Expense.amount))
        .filter(Expense.date >= start_date, Expense.date <= end_date)
        .group_by(Expense.category)
        .all()
    )
    return {category: total for category, total in results}

@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.get(Expense, expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db_expense.amount = expense.amount
    db_expense.category = expense.category
    db_expense.date = expense.date
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.get(Expense, expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
