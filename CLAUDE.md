# CLAUDE.md

## Overview
A personal expense tracker backend built with FastAPI. Tracks
individual expenses (not budgets) with amount, category, and date.

## Data Model
Expense:
- id: unique identifier, auto-assigned by the database
- amount: number (the expense amount)
- category: text, must be one of a fixed set of valid categories
  (groceries, transport, entertainment, utilities, rent, healthcare, other)
- date: the date the expense occurred

## Storage
SQLite database (not a flat JSON file like the earlier todo-app project).

## API Design
FastAPI routes following REST conventions:
- POST /expenses - create a new expense
- GET /expenses - list all expenses
- DELETE /expenses/{id} - delete a specific expense by its id

No update/edit functionality yet (may be added later).

## Categories
Categories are a fixed, predefined set - not free text - to avoid
inconsistent/duplicate category names from typos.