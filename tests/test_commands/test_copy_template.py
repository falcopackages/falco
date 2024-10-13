from __future__ import annotations

import pytest
from django.apps import apps
from django.core.management import call_command
from django.core.management import CommandError
from django.test import override_settings
from falco.management.commands.copy_template import Command
from falco.management.commands.copy_template import get_template_absolute_path


@pytest.fixture
def command():
    return Command()


@pytest.fixture
def template_dirs(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    source_dir = tmp_path / "source_templates"
    source_dir.mkdir()

    with override_settings(
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [str(template_dir), str(source_dir)],
            }
        ]
    ):
        yield template_dir, source_dir


@pytest.fixture
def create_template(template_dirs):
    def _create_template(name, content):
        _, source_dir = template_dirs
        template_path = source_dir / name
        template_path.write_text(content)
        return template_path

    return _create_template


def test_get_template_absolute_path(create_template):
    template_path = create_template("test_template.html", "<h1>Test Template</h1>")

    result = get_template_absolute_path("test_template.html")

    assert result == str(template_path)


def test_get_template_absolute_path_not_found():
    with pytest.raises(CommandError):
        get_template_absolute_path("non_existent_template.html")

    # assert result is None


def test_copy_template_with_destination(tmp_path, create_template):
    create_template("source_template.html", "<p>Source Template</p>")

    app_config = apps.get_app_config("books")

    app_dir = tmp_path / app_config.label
    app_dir.mkdir()

    with override_settings(BASE_DIR=tmp_path):
        original_path = app_config.path
        app_config.path = str(app_dir)

        call_command("copy_template", "source_template.html", "books")

        app_config.path = original_path

    copied_template = app_dir / "templates" / "source_template.html"

    assert copied_template.exists()
    assert copied_template.read_text() == "<p>Source Template</p>"


def test_copy_template_without_destination(tmp_path, create_template):
    create_template("source_template.html", "<p>Source Template</p>")

    with override_settings(BASE_DIR=tmp_path):
        call_command("copy_template", "source_template.html")

    copied_template = tmp_path / "templates" / "source_template.html"

    assert copied_template.exists()
    assert copied_template.read_text() == "<p>Source Template</p>"


def test_copy_template_without_destination_and_templates_setting(tmp_path, create_template):
    create_template("source_template.html", "<p>Source Template</p>")

    with override_settings(BASE_DIR=tmp_path, TEMPLATES=[]):
        # out = StringIO()
        with pytest.raises(CommandError):
            call_command("copy_template", "source_template.html")
    #     output = out.getvalue().strip()
    #
    # copied_template = tmp_path / "templates" / "source_template.html"
    #
    # assert output == "Source Template doesn't exist"
    # assert not copied_template.exists()


def test_copy_template_source_not_found(template_dirs):
    # out = StringIO()
    with pytest.raises(CommandError):
        call_command("copy_template", "nonexistent_template.html")
    # output = out.getvalue().strip()
    #
    # template_dir, _ = template_dirs
    # copied_template = template_dir / "nonexistent_template.html"
    #
    # assert output == "Source Template doesn't exist"
    # assert not copied_template.exists()
