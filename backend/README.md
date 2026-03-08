# Intelligent Expense Tracker — Backend

Django REST API with JWT auth, PostgreSQL, expense management, analytics, and bank statement parsing.

## Setup

1. Create virtualenv and install deps:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set:
   - `SECRET_KEY`
   - `DATABASE_URL=postgresql://user:password@localhost:5432/expense_tracker`
   - `CORS_ALLOWED_ORIGINS=http://localhost:5173`

3. Run migrations and seed categories:
   ```bash
   python manage.py migrate
   python manage.py seed_categories
   ```

4. Run server:
   ```bash
   python manage.py runserver
   ```

## API Docs

- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/

## Docker

```bash
docker build -t expense-backend .
docker run -p 8000:8000 -e DATABASE_URL=... -e SECRET_KEY=... expense-backend
```
