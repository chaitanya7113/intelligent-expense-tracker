# PocketLens Expense Tracker — Architecture

## System Overview

The **PocketLens Expense Tracker** is a full-stack application that lets users track expenses, upload bank statements (CSV), and view analytics. The backend is Django REST with JWT auth and PostgreSQL; the frontend is React (Vite) with charts and JWT in localStorage.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React + Vite)                         │
│  Login │ Register │ Dashboard │ Add Expense │ Expense List │ Analytics  │
│  Axios + JWT (localStorage) │ Chart.js/Recharts                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS / REST API
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    BACKEND (Django + DRF)                               │
│  JWT Auth │ Expenses API │ Analytics │ Statement Upload │ Categorization│
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PostgreSQL                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Backend Architecture (Django)

### Layered Structure

Business logic is separated into clear layers so that views stay thin and logic is testable and reusable.

| Layer        | Purpose |
|-------------|---------|
| **models/** | Django models (User, Expense, Category, TransactionSource, etc.) |
| **serializers/** | DRF serializers for request/response validation and transformation |
| **views/**  | HTTP handlers; delegate to services and return serialized responses |
| **services/** | Business logic (expense CRUD, analytics, parsing, categorization) |
| **utils/**  | Helpers (logging, parsing, validation) |
| **routes**  | URL routing (urls.py) wiring views to endpoints |

### Backend Folder Structure

```
backend/
├── config/                    # Django project config
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py                # Root URL config
│   └── wsgi.py
├── apps/
│   ├── users/                 # User & auth
│   │   ├── models/
│   │   ├── serializers/
│   │   ├── views/
│   │   ├── services/
│   │   └── urls.py
│   ├── expenses/              # Expense CRUD & analytics
│   │   ├── models/
│   │   ├── serializers/
│   │   ├── views/
│   │   ├── services/
│   │   └── urls.py
│   ├── transactions/          # Bank statements & categorization
│   │   ├── models/
│   │   ├── serializers/
│   │   ├── views/
│   │   ├── services/
│   │   └── urls.py
│   └── categories/            # Category model & lookup
│       ├── models/
│       └── (used by expenses/transactions)
├── core/                      # Shared utilities
│   ├── utils/
│   ├── exceptions.py
│   └── logging_config.py
├── manage.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

### API Endpoints (Conceptual)

| Area        | Method | Endpoint (example)        | Description |
|------------|--------|----------------------------|-------------|
| Auth       | POST   | /api/auth/register/        | Register |
| Auth       | POST   | /api/auth/login/           | Login (JWT) |
| Auth       | POST   | /api/auth/token/refresh/   | Refresh JWT |
| Expenses   | GET    | /api/expenses/             | List (filter, paginate) |
| Expenses   | POST   | /api/expenses/             | Create |
| Expenses   | GET    | /api/expenses/:id/         | Retrieve |
| Expenses   | PUT    | /api/expenses/:id/         | Update |
| Expenses   | DELETE | /api/expenses/:id/         | Delete |
| Analytics  | GET    | /api/analytics/summary/    | Monthly summary |
| Analytics  | GET    | /api/analytics/by-category/| Category breakdown |
| Analytics  | GET    | /api/analytics/monthly-comparison/ | Monthly comparison |
| Statements | POST   | /api/statements/upload/    | Upload CSV, parse, store |

---

## Frontend Architecture (React + Vite)

### Folder Structure

```
frontend/
├── public/
├── src/
│   ├── api/                   # Axios instance + API functions
│   │   ├── client.js
│   │   └── endpoints.js
│   ├── components/            # Reusable UI
│   │   ├── common/
│   │   └── layout/
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── AddExpense.jsx
│   │   ├── ExpenseList.jsx
│   │   └── Analytics.jsx
│   ├── context/               # Auth context (user, token)
│   ├── hooks/
│   ├── utils/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── vite.config.js
├── package.json
└── README.md
```

### Data Flow

- **Auth**: Login/Register → store JWT in localStorage → set token on Axios default header.
- **Protected routes**: Check token; redirect to Login if missing.
- **API calls**: Axios client reads token from localStorage and sends `Authorization: Bearer <token>`.

---

## Database Models (Summary)

- **User** — Django’s AbstractUser (or custom user); used for ownership of expenses/transactions.
- **Category** — Name (e.g. Food, Travel, Shopping); used for expenses and auto-categorization.
- **TransactionSource** — Bank or Credit card; links uploaded statements.
- **Expense** — Manual entries: amount, date, category, description, user.
- **Transaction** — Parsed from CSV: date, description, amount, debit/credit, source, category (optional, can be auto-filled).

---

## Security & Deployment

- **Secrets**: All secrets and DB URL in environment variables; `.env` not committed.
- **JWT**: Access + refresh tokens; short-lived access token.
- **CORS**: Configured for frontend origin in production.
- **Docker**: Backend Dockerfile for containerization; optional docker-compose for backend + DB + frontend.

---

## Next Steps

1. Implement backend: models → serializers → services → views → urls → settings.
2. Implement frontend: API client → auth context → pages → routing.
3. Add Swagger/OpenAPI (e.g. drf-spectacular) and Docker/env as specified.
