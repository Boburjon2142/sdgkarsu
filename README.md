# Premium Institutional Django Portal

Official-grade multi-page institutional website built with Django, Django templates, custom CSS, SQLite by default, and an admin-managed content model.

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
3. Copy `.env.example` to `.env` and adjust values for your machine if needed.
4. Apply migrations:
   `python manage.py migrate`
5. Create admin user:
   `python manage.py createsuperuser`
6. Run development server:
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
3. Set environment variables based on `.env.example`, especially:
   `DJANGO_SECRET_KEY`
   `DJANGO_DEBUG=0`
   `DJANGO_ALLOWED_HOSTS`
   `DJANGO_CSRF_TRUSTED_ORIGINS`
   `DATABASE_URL` if you are not using SQLite
4. Run:
   `python manage.py migrate`
   `python manage.py collectstatic --noinput`
5. Run a production readiness check:
   `python manage.py check --deploy`
6. Configure the web app to point to `config.wsgi`.
7. Add static root mapping to `/static/` -> `staticfiles`.
8. Add media root mapping to `/media/` -> `media`.
9. Reload the PythonAnywhere web app.
10. If you want the site to open with ready demo cards, images, and SDG content, run:
   `python manage.py load_demo_content --reset`

## Demo content on PythonAnywhere

- Demo images are bundled inside `assets/images/` and are tracked by git.
- Uploaded runtime files inside `media/` stay ignored by git, so the repository remains clean.
- After deployment, run:
  `python manage.py migrate`
  `python manage.py load_demo_content --reset`
- This command copies bundled demo images into the proper media folders and creates sample:
  - leader photo
  - news articles
  - SDG work items

## Environment variables

- `DJANGO_SECRET_KEY`: required in production
- `DJANGO_DEBUG`: use `0` in production
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames
- `DJANGO_CSRF_TRUSTED_ORIGINS`: comma-separated HTTPS origins
- `DATABASE_URL`: optional, supports `sqlite:///...`, `postgres://...`, `postgresql://...`, and `mysql://...`
- `DJANGO_DB_CONN_MAX_AGE`: database connection lifetime in seconds
- `DJANGO_SECURE_SSL_REDIRECT`: defaults to `1` in production
- `DJANGO_SECURE_HSTS_SECONDS`: defaults to `31536000` in production
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`: defaults to `1` in production
- `DJANGO_SECURE_HSTS_PRELOAD`: defaults to `1` in production

## Production notes

- The project loads variables from `.env` automatically if the file exists.
- Production mode now refuses to start with the default secret key.
- Production mode now refuses to start without `DJANGO_ALLOWED_HOSTS`.
- Security defaults are enabled automatically when `DJANGO_DEBUG=0`.
- Use `python manage.py check --deploy` before going live.
- The project includes `robots.txt` and `sitemap.xml`
- Media and static paths are already configured for PythonAnywhere
