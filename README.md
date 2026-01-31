# Diani Connect

A service marketplace connecting customers with local providers in Kwale County, Kenya. Built with Django, server-rendered templates, HTMX interactivity, and Tailwind CSS.

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

## Demo Credentials

| Role | Username | Password |
| --- | --- | --- |
| Customer | `customer_demo` | `customer123` |
| Provider | `provider_demo` | `provider123` |
| Admin | `admin_demo` | `admin123` |

## Features

- Service browsing with HTMX live filters (area, category, keyword)
- Provider CRUD for listings
- Booking requests with status tracking
- Reviews after completed bookings
- Admin moderation panel at `/moderation`
- Blog and contact pages

## Environment Configuration

Create a `.env` file to override defaults:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

Postgres-ready settings are included; swap DB_* values for production.
