# Recipe API (TDD)

A Django project built test-first as the foundation for a recipe API. Today it contains an email-based custom user model, its Django admin, and the test suite that drove them. Recipes, ingredients, tags and API endpoints are **not implemented yet**; DRF is installed for that next step.

## What exists

- `core.User`: custom user with email as the login field (normalized, unique), `name`, `is_active`, `is_staff`, and permissions via `PermissionsMixin`.
- `UserManager.create_user` / `create_superuser`; a missing email raises `ValueError`.
- Django admin for users (list, change, add pages), at `/admin/`.
- 14 tests covering the model, manager, admin pages, and the settings helpers.

## Stack

Python 3.13, Django 5.2 LTS, Django REST Framework (installed, unused so far), PostgreSQL 17 via Docker (SQLite when no database is configured), gunicorn. Versions: [VERSIONS.md](./VERSIONS.md).

## Quickstart (Docker)

```bash
git clone https://github.com/kneeraazon404/recipe-api-tdd.git
cd recipe-api-tdd
cp .env.example .env     # set DJANGO_SECRET_KEY and POSTGRES_PASSWORD
docker compose up --build
docker compose run --rm app python manage.py createsuperuser
```

Open http://localhost:8000/admin/.

## Quickstart (local, uv)

Requires [uv](https://docs.astral.sh/uv/). Without `DATABASE_URL` or `DB_HOST` the app uses SQLite.

```bash
export DJANGO_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')"
export DJANGO_DEBUG=true
uv sync
cd app
uv run python manage.py migrate
uv run python manage.py runserver
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | required | startup fails without it |
| `DJANGO_DEBUG` | `false` | debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | comma-separated hosts |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | empty | comma-separated origins |
| `DATABASE_URL` | none | any dj-database-url URL; takes priority |
| `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` | none | original variables; build a PostgreSQL URL (used by docker-compose) |

When `DJANGO_DEBUG=false` the app also enables HTTPS redirect, secure cookies and HSTS (`DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_HSTS_SECONDS`).

## Testing

```bash
uv run pytest -q
uv run ruff check . && uv run ruff format --check .
```

Tests run against in-memory SQLite (`app/app/settings_test.py`). CI: `.github/workflows/ci.yml` (replaces the old Travis config).

## Project structure

```
app/
  app/        settings, urls, wsgi/asgi, settings_test.py
  core/       custom User model, admin, migrations, tests/
  manage.py
Dockerfile, docker-compose.yml   production-style image (gunicorn) and local Postgres stack
pyproject.toml, uv.lock          dependencies (requirements.txt is exported)
```

## License

MIT. See [LICENSE](LICENSE).
