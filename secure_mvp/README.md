# Secure MVP Stack

This folder contains a production-structured starter built with:

- Backend: Django + Django REST Framework
- Frontend: Next.js App Router
- Database: PostgreSQL in production
- Authentication: secure server-side sessions with CSRF protection

## Why I chose session auth

For a browser-based app, session auth is usually safer than JWT stored in `localStorage`.

Why:

- the browser keeps the session id in an `HttpOnly` cookie
- the backend can revoke sessions immediately
- there is less custom token lifecycle logic to get wrong
- Django already provides mature CSRF protections

This project is designed for first-party frontend/backend deployments such as:

- `app.example.com` for Next.js
- `api.example.com` for Django

## Security defaults included

- custom user model with role field
- RBAC checks on sensitive endpoints
- object-level project access control to reduce IDOR risk
- strict serializers to prevent mass assignment
- file upload validation for type, extension, and size
- DRF throttling for login, registration, and sensitive actions
- safe API exception handling
- pagination on list endpoints
- structured logging
- audit trail model for auth and project actions
- production security headers
- strict CORS and CSRF origin config
- environment variables for all secrets

## Folder structure

- `backend/`: Django REST API
- `frontend/`: Next.js frontend

## Backend quick start

1. Create a PostgreSQL database.
2. Copy `backend/.env.example` to `backend/.env`.
3. Install backend dependencies.
4. Run migrations.
5. Create a superuser.
6. Start Django.

## Frontend quick start

1. Copy `frontend/.env.example` to `frontend/.env.local`.
2. Set `NEXT_PUBLIC_API_BASE_URL`.
3. Install frontend dependencies.
4. Start Next.js.

## Deployment notes

### Backend

Good targets:

- Render
- Railway
- PythonAnywhere

Required before go-live:

- `DJANGO_DEBUG=0`
- PostgreSQL connection via `DATABASE_URL`
- correct `DJANGO_ALLOWED_HOSTS`
- exact `DJANGO_CORS_ALLOWED_ORIGINS`
- exact `DJANGO_CSRF_TRUSTED_ORIGINS`
- HTTPS enabled
- `python manage.py check --deploy`

### Frontend

Good target:

- Vercel

Important:

- never put secrets in `NEXT_PUBLIC_*`
- only expose the backend base URL publicly
- keep all sensitive checks in the backend API

## Dependency and code hygiene

Dependencies were kept intentionally small:

- backend: Django, DRF, `django-cors-headers`, `psycopg`, Pillow
- frontend: Next.js, React, React DOM

Recommended CI/CD security scans:

- backend dependency scan:
  `pip-audit`
- optional second Python package scan:
  `safety check`
- Python static security scan:
  `bandit -r backend`
- Django deploy checks:
  `python manage.py check --deploy`
- frontend dependency audit:
  `npm audit --production`

Best place to run them:

- on every pull request
- on the default branch after merge
- before production deployment

## Tested in this workspace

- backend startup checks
- backend deploy checks
- auth and project permission tests

The frontend scaffold is generated and ready to connect, but Node install/build was not run in this workspace.
