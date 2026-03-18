# Premium Institutional Django Portal

Official-grade multi-page institutional website built with Django, Django templates, custom CSS, SQLite, and an admin-managed content model.

## Project architecture

- `config/`: Django settings, URL routing, WSGI, ASGI
- `portal/`: reusable portal app with models, admin, forms, views, URLs, sitemap, tests, and seed migration
- `templates/portal/`: multi-page institutional templates
- `assets/css/`, `assets/js/`: custom design system and interaction layer
- `media/`: uploaded reports and policy files

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Apply migrations:
   `python manage.py migrate`
4. Create admin user:
   `python manage.py createsuperuser`
5. Run development server:
   `python manage.py runserver`

Seed content is included in the `portal` migrations so the homepage and all core sections render immediately after migration.

## Admin-managed content

The admin panel allows editors to manage:

- Site settings and homepage hero
- Page intro blocks and SEO fields
- Hero stats and institutional values
- Strategic priorities and governance roles
- Programs, research projects, and education initiatives
- Policy documents and reports
- Metrics, achievements, partners, news, and events
- Department contacts and contact submissions

## PythonAnywhere deployment

1. Upload the project or clone it into your PythonAnywhere account.
2. Create a virtual environment and install dependencies:
   `pip install -r requirements.txt`
3. Set environment variables based on `.env.example`.
4. Run:
   `python manage.py migrate`
   `python manage.py collectstatic --noinput`
5. Configure the web app to point to `config.wsgi`.
6. Add static root mapping to `/static/` -> `staticfiles`.
7. Add media root mapping to `/media/` -> `media`.
8. Reload the PythonAnywhere web app.

## Production notes

- Set `DJANGO_DEBUG=0`
- Use a strong `DJANGO_SECRET_KEY`
- Set `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`
- The project includes `robots.txt` and `sitemap.xml`
- Media and static paths are already configured for PythonAnywhere
