# myapp/management/commands/rm_migrations.py
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from rich import print as rich_print
from rich.progress import track

class Command(BaseCommand):
    help = 'Remove all migrations for the specified applications directory, intended only for development.'

    def add_arguments(self, parser):
        parser.add_argument(
            'apps_dir',
            type=Path,
            nargs='?',
            default=None,
            help='The path to your Django apps directory.'
        )
        parser.add_argument(
            '--skip-git-check',
            action='store_true',
            help='Do not check if your git repo is clean.'
        )

    def handle(self, *args, **options):
        apps_dir = options['apps_dir']
        skip_git_check = options['skip_git_check']

        if not settings.DEBUG:
            raise CommandError('This command can only be run with DEBUG=True.')

        if not apps_dir:
            apps_dir = Path(settings.BASE_DIR)

        if not skip_git_check:
            self.check_git_repo_clean()

        apps = set()
        for folder in track(apps_dir.iterdir(), description="Removing migration files"):
            migration_dir = folder / 'migrations'
            if not migration_dir.exists():
                continue
            apps.add(folder.stem)
            for file in migration_dir.iterdir():
                if file.suffix == '.py' and file.name != '__init__.py':
                    file.unlink()

        apps_ = ', '.join(apps)
        rich_print(f'[green]Removed migration files for apps: {apps_}')

    def check_git_repo_clean(self):
        import subprocess
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout:
            raise CommandError('Your git repository is not clean. Commit or stash your changes before running this command.')
