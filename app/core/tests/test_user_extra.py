import subprocess
import sys

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from app import settings

User = get_user_model()


@pytest.mark.django_db
def test_str_is_email():
    assert str(User.objects.create_user("a@example.com", "pw-12345-xyz")) == "a@example.com"


@pytest.mark.django_db
def test_extra_fields_are_stored_and_defaults():
    user = User.objects.create_user("a@example.com", "pw-12345-xyz", name="Ann")
    assert user.name == "Ann"
    assert user.is_active and not user.is_staff and not user.is_superuser


@pytest.mark.django_db
def test_email_must_be_unique():
    User.objects.create_user("a@example.com", "pw-12345-xyz")
    with pytest.raises(IntegrityError):
        User.objects.create_user("a@example.com", "other-pw-1")


@pytest.mark.django_db
def test_login_uses_email_not_username(client):
    User.objects.create_user("a@example.com", "pw-12345-xyz")
    assert client.login(email="a@example.com", password="pw-12345-xyz")
    assert not client.login(email="a@example.com", password="wrong")


def test_legacy_db_env_builds_postgres_url(monkeypatch):
    monkeypatch.setenv("DB_HOST", "db")
    monkeypatch.setenv("DB_NAME", "app")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASS", "p@ss/word")
    assert settings._legacy_database_url() == "postgres://postgres:p%40ss%2Fword@db/app"


def test_without_db_host_falls_back_to_sqlite(monkeypatch):
    monkeypatch.delenv("DB_HOST", raising=False)
    assert settings._legacy_database_url().startswith("sqlite:///")


def test_missing_secret_key_fails_fast():
    code = "import os; os.environ.pop('DJANGO_SECRET_KEY', None); import app.settings"
    result = subprocess.run(
        [sys.executable, "-c", code], cwd="app", capture_output=True, text=True, check=False
    )
    assert result.returncode != 0
    assert "DJANGO_SECRET_KEY" in result.stderr
