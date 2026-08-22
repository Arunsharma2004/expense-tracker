# CLAUDE.md

## Overview
A personal expense tracker backend built with FastAPI. Tracks
individual expenses (amount, category, date) and monthly budgets
per category, and can report spending summaries.

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
- PUT /expenses/{id} - update a specific expense by its id
- DELETE /expenses/{id} - delete a specific expense by its id
- POST /budgets - create a budget for a category/month/year
- GET /budgets - check budget status (spent/remaining) for a category/month/year
- GET /summary - get total spending per category for a given month/year

## Categories
Categories are a fixed, predefined set - not free text - to avoid
inconsistent/duplicate category names from typos.

## Known Limitations
- Tests in test_main.py share the same database (expenses.db) and aren't isolated from
  each other - setup data from one test (e.g. a valid expense created before testing an
  invalid update) can leak into and affect assertions in unrelated tests (e.g.
  test_check_budget's spending totals). A proper fix would use a separate, isolated test
  database (possibly in-memory SQLite) that resets between each test, so tests never
  depend on or interfere with each other's data. Currently worked around by using >=
  instead of == in assertions sensitive to totals.

## Future Improvements
- Consider adopting the `Annotated` dependency alias pattern (e.g.
  `SessionDep = Annotated[Session, Depends(get_db)]` in deps.py) instead of
  repeating `Session = Depends(get_db)` in every route signature - seen in
  tiangolo/full-stack-fastapi-template during Day 17 codebase exploration.
  Reduces duplication similar to the resolve_task helper pattern from Day 10.

## Lessons Learned
- SQLite uses type affinity, not strict enforcement - schemas.py (Pydantic)
  is the real type enforcement layer, not models.py.
- Always check terminal/server logs for the real error behind a 500 Internal
  Server Error, since the client-facing message hides details for security.
- A 200/successful status code doesn't guarantee correctness - silent logic
  bugs like boundary condition errors can produce valid-looking wrong
  responses.