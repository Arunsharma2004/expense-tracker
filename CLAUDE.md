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

## Lessons Learned
- SQLite uses type affinity, not strict enforcement - schemas.py (Pydantic)
  is the real type enforcement layer, not models.py.
- Always check terminal/server logs for the real error behind a 500 Internal
  Server Error, since the client-facing message hides details for security.
- A 200/successful status code doesn't guarantee correctness - silent logic
  bugs like boundary condition errors can produce valid-looking wrong
  responses.