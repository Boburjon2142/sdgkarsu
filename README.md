# SDG Portal

Backend-powered university sustainability portal built with Django.

## Local setup

1. Install dependencies:
   `pip install -r requirements.txt`
2. Run migrations:
   `python manage.py migrate`
3. Create an admin user:
   `python manage.py createsuperuser`
4. Start the server:
   `python manage.py runserver`

Seed data is loaded automatically by the `portal` app migrations.

## PythonAnywhere notes

1. Create a virtualenv and install `requirements.txt`.
2. Set the WSGI file to point at `config.wsgi`.
3. Set environment variables:
   `DJANGO_SECRET_KEY`
   `DJANGO_DEBUG=0`
   `DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com`
   `DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com`
4. Run:
   `python manage.py migrate`
   `python manage.py collectstatic --noinput`

Static files are collected from `assets/` into `staticfiles/`.
