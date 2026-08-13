# Expense Tracker

A personal expense tracker backend built with FastAPI. It tracks individual
expenses (not budgets) — each with an amount, a category, and a date — and
stores them in a SQLite database.

## Data model

Each expense has:

- **id** — unique identifier, auto-assigned by the database
- **amount** — the expense amount (must be greater than 0)
- **category** — one of a fixed set: `groceries`, `transport`,
  `entertainment`, `utilities`, `rent`, `healthcare`, `other`
- **date** — the date the expense occurred (`YYYY-MM-DD`)

Categories are a fixed, predefined set rather than free text, to avoid
inconsistent or duplicate category names from typos.

## Setup

Requires Python 3.10+.

```bash
# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# install dependencies
pip install -r requirements.txt
```

## Running the app

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, and interactive docs
(Swagger UI) at `http://127.0.0.1:8000/docs`.

A SQLite database file (`expenses.db`) is created automatically in the
project root on first run.

## Running the tests

```bash
pytest
```

## Endpoints

### `POST /expenses`

Create a new expense.

**Request**

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.50, "category": "groceries", "date": "2026-08-12"}'
```

**Response** — `201 Created`

```json
{
  "amount": 25.5,
  "category": "groceries",
  "date": "2026-08-12",
  "id": 1
}
```

### `GET /expenses`

List all expenses.

**Request**

```bash
curl http://127.0.0.1:8000/expenses
```

**Response** — `200 OK`

```json
[
  {
    "amount": 25.5,
    "category": "groceries",
    "date": "2026-08-12",
    "id": 1
  }
]
```

### `DELETE /expenses/{id}`

Delete a specific expense by its id.

**Request**

```bash
curl -X DELETE http://127.0.0.1:8000/expenses/1
```

**Response** — `204 No Content` on success, `404 Not Found` if no expense
with that id exists.

### `GET /summary`

Get total spending per category for a given month and year. Only
categories with at least one expense in that period are included.

**Request**

```bash
curl "http://127.0.0.1:8000/summary?month=8&year=2026"
```

**Response** — `200 OK`

```json
{
  "groceries": 150.0,
  "transport": 30.0
}
```

---

Built with [Claude Code](https://claude.com/claude-code).
