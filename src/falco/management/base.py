from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from falco.utils import clean_git_repo


def get_apps_dir() -> Path:
    try:
        return settings.APPS_DIR
    except AttributeError:
        msg = "Add an APPS_DIR settings, eg: APPS_DIR = BASE / 'apps'"
        raise CommandError(msg)


def exit_if_debug_false():
    if not settings.DEBUG:
        msg = "Nope, not happening, this command can only be run with DEBUG=True."
        raise CommandError(msg)


class CleanRepoOnlyCommand(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--allow-dirty", action="store_true", help="Allow dirty git repo."
        )
        super().add_arguments(parser)

    def handle(self, *args, **options):
        allow_dirty = options["allow_dirty"]
        if not clean_git_repo() and not allow_dirty:
            msg = "Git repo is not clean, clean or stash away changes before running this command"
            raise CommandError(msg)
        return super().handle(*args, **options)
