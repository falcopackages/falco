import subprocess
from pathlib import Path

import pytest

from django.core.management import call_command

blog_app_path = Path(__file__).parent.parent / "blog"
#pytestmark = pytest.mark.django_db
from django.apps import apps
def test_rm_migrations(set_git_repo_to_clean, settings, transactional_db):
    settings.DEBUG = True
    apps.clear_cache()
    call_command("makemigrations", "blog")
    first_migration = blog_app_path / "migrations/0001_initial.py"
    print(first_migration)
    assert first_migration.exists()
    call_command("rm_migrations", "blog")
    assert not first_migration.exists()


# def test_rm_migrations_fake_apps_dir(set_git_repo_to_clean):
#     apps_dir = Path()
#     call_command("makemigrations")
#     first_migration = apps_dir / "blog/migrations/0001_initial.py"
#     assert first_migration.exists()
#     call_command("rm_migrations", "myproject")
#     assert first_migration.exists()


# def test_rm_migrations_not_clean_repo(django_project):
#     with pytest.raises(cappa.Exit):
#         runner.invoke("rm_migrations", ".")
