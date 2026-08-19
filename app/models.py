import enum

from sqlalchemy import Column, Date, Enum, Float, Integer

from app.database import Base


class Category(str, enum.Enum):
    groceries = "groceries"
    transport = "transport"
    entertainment = "entertainment"
    utilities = "utilities"
    rent = "rent"
    healthcare = "healthcare"
    other = "other"


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    category = Column(Enum(Category), nullable=False)
    date = Column(Date, nullable=False)


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Enum(Category), nullable=False)
    amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
