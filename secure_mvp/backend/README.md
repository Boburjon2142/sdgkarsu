# Secure MVP Backend

Production-oriented Django REST Framework backend with:

- PostgreSQL-only runtime configuration
- Secure session-based authentication for browser clients
- CSRF protection and tightly scoped CORS
- Role-based access control
- DRF throttling on authentication and sensitive endpoints
- Audit logging for important actions
- File upload validation
- Deployment-safe settings via environment variables

## Why session auth here?

For a browser-first application, server-side sessions are usually safer than storing JWTs in `localStorage` because:

- the session identifier stays in an `HttpOnly` cookie
- sessions are easy to revoke server-side
- there is no custom token rotation logic to get wrong
- Django gives strong CSRF protections out of the box

For cross-origin deployments like `app.example.com` and `api.example.com`, use secure cookies, HTTPS, and explicit CORS/CSRF origin settings.

## Local setup

1. Create PostgreSQL database.
2. Copy `.env.example` to `.env`.
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create admin: `python manage.py createsuperuser`
6. Start server: `python manage.py runserver`

## Production checklist

- `DJANGO_DEBUG=0`
- long random `DJANGO_SECRET_KEY`
- strict `DJANGO_ALLOWED_HOSTS`
- exact `DJANGO_CORS_ALLOWED_ORIGINS`
- exact `DJANGO_CSRF_TRUSTED_ORIGINS`
- PostgreSQL user with least privileges
- `python manage.py check --deploy`
