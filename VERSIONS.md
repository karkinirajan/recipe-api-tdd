# Versions

Resolved in `uv.lock` on 2026-10-29. "Previous" is the old `requirements.txt` / Dockerfile / compose file.

| Component | Version | Previous | Note |
|---|---|---|---|
| Python | 3.13 (`.python-version`; image `python:3.13-slim`) | 3.7 (Docker), 3.6 (Travis) | |
| Django | 5.2.18 | 3.0.6 | 5.2 is the LTS line (6.1.x is newer but not LTS) |
| djangorestframework | 3.18.3 | 3.12.2 | installed, not used yet |
| dj-database-url | 3.1.2 | n/a | new |
| psycopg | 3.3.6 (binary) | psycopg2 2.8.6 | |
| gunicorn | 26.2.0 | n/a | new, used by the image |
| PostgreSQL (compose) | 17-alpine | 10-alpine | not verified as the newest major |
| uv (image copy) | 0.13.6 | n/a | pinned to the version used to build and test |
| flake8 | removed | >=3.6,<3.7 | replaced by ruff |

Dev: pytest, pytest-django, ruff.
