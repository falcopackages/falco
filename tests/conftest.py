import os
import logging
import subprocess
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
from django.conf import settings

import pytest
from .settings import DEFAULT_SETTINGS


def pytest_configure(config):
    settings.configure(**DEFAULT_SETTINGS, **TEST_SETTINGS)


TEST_SETTINGS = {
    "INSTALLED_APPS": [
        "falco",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "tests.blog",
    ],
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [Path(__file__).parent / "templates"],
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                ],
                "loaders": [
                    (
                        "template_partials.loader.Loader",
                        [
                            "django.template.loaders.filesystem.Loader",
                            "django.template.loaders.app_directories.Loader",
                        ],
                    )
                ],
            },
        }
    ],
}


@pytest.fixture
def blog_app(tmp_path, settings):
    blog_app = tmp_path / "blog"
    blog_app.mkdir()
    models_py = blog_app / "models.py"
    models_py.write_text(
        """
from django.db import models
from falco.models import TimeStamped

class Post(TimeStamped):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
        """
    )
    # settings.INSTALLED_APPS.append("blog")
    yield blog_app
    models_py.unlink()
    blog_app.rmdir()

@pytest.fixture
def set_git_repo_to_clean():
    def mock_run(args, **kwargs):
        if args == ["git", "status", "--porcelain"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = ""
            return mock
        return original_run(args, **kwargs)

    original_run = subprocess.run

    with patch("subprocess.run", side_effect=mock_run):
        yield


@pytest.fixture
def pyproject_toml(tmp_path):
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text(
        """
        [project]
        name = "myproject"
        version = "0.1.0"
        """
    )
    yield pyproject_toml
    pyproject_toml.unlink()


@pytest.fixture
def git_user_infos():
    name = "John Doe"
    email = "johndoe@example.com"

    def mock_run(args, **kwargs):
        if args == ["git", "config", "--global", "--get", "user.name"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = name
            return mock
        if args == ["git", "config", "--global", "--get", "user.email"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = email
            return mock

        return original_run(args, **kwargs)

    original_run = subprocess.run

    with patch("subprocess.run", side_effect=mock_run):
        yield name, email
