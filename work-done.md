# Work done: recipe-api-tdd

Branch: `chore/modernize` (local, not pushed). Date: 2026-10-29. The repo had no uncommitted work.

## What was there
A Django 3.0 project in `app/` (project `app`, app `core`) on Python 3.7, with a Docker/compose dev stack (PostgreSQL 10) and a Travis CI file. It contains only an email-based custom `User` model, its admin, and 7 tests. The README described a full recipe/ingredient/tag API that does not exist. `settings.py` had a hardcoded secret key and `DEBUG = True`; compose hardcoded a database password.

## Changes by file
| File | Before | Change |
|---|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | absent | New uv project, Python 3.13, Django 5.2 LTS, DRF, psycopg 3, gunicorn |
| `requirements.txt` | 4 pins incl. flake8 | Exported from lockfile |
| `app/app/settings.py` | hardcoded secret, DEBUG True, empty ALLOWED_HOSTS, Postgres-only, `USE_L10N` | Env-driven secret (fails fast if missing), DEBUG, ALLOWED_HOSTS; `DATABASE_URL`, with the original `DB_*` variables still supported and SQLite fallback; `DEFAULT_AUTO_FIELD` pinned to match the existing migration; `STATIC_ROOT`; CSRF origins; HTTPS/HSTS/secure cookies when not debug; `USE_L10N` removed |
| `app/app/settings_test.py` | absent | New |
| `app/core/models.py` | no `__str__` | `User.__str__` returns the email |
| `app/core/tests/test_user_extra.py` | absent | New: 7 tests (str, defaults, unique email, email login, DB URL building, SQLite fallback, fail-fast on missing secret) |
| `app/core/tests/test_admin.py`, other `.py` | mixed formatting | `ruff format` / import sort only |
| `Dockerfile` | python:3.7-alpine, build toolchain, dev server | python:3.13-slim, uv sync from the lockfile (uv image pinned to 0.13.6), non-root user, gunicorn |
| `docker-compose.yml` | hardcoded DB password, Postgres 10, no healthcheck | Secrets from `.env` (compose refuses to start without them), Postgres 17 with healthcheck and a named volume, migrate on start |
| `.env.example`, `.github/workflows/ci.yml` | absent | New |
| `.travis.yml` | Travis CI (Python 3.6, docker-compose) | Deleted; replaced by the GitHub Actions workflow |
| `.vscode/settings.json` | tracked | Untracked |
| `.gitignore` | basics | Also ignores `.vscode/`, `.env`, `staticfiles/`, caches |
| `README.md` | described features that do not exist | Rewritten to describe what exists, how to run it, and config |
| `VERSIONS.md`, `work-done.md` | absent | New |

## Bug found by a test and fixed
My first version of the compose-compatible DB URL helper used `urllib.parse.quote` with its default `safe="/"`, so a password containing `/` would have produced a broken URL. The test caught it; the helper now escapes everything.

## Verification (actual runs)
- `uv run pytest -q`: 14 passed (the original 7 pass unchanged on Django 5.2).
- `uv run ruff check .` and `ruff format --check .`: clean.
- `manage.py check` and `makemigrations --check`: no issues, no changes.
- `docker compose config` validates with env set, and correctly errors without it.
- `docker build` succeeded and `manage.py check` ran inside the image; the test image was removed afterwards.
- Not run: `docker compose up` against the PostgreSQL service, and `check --deploy`.

## Needs your attention
- The old secret key and the compose database password (a dev value) are in git history.
- The recipe API itself (recipes, ingredients, tags, auth endpoints) is not built; DRF is a dependency waiting for it.
- Nothing pushed. To publish: `git push -u origin chore/modernize`
