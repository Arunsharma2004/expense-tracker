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
