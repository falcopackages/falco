import subprocess
from django.core.management.base import BaseCommand, CommandError



class GitAwareBaseCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--allow-dirty',
            action='store_true',
            help='Do not check if your git repo is clean.',
            default=False
        )

    def handle(self, *args, **options) -> str | None:
        allow_dirty = options['allow_dirty']
        if not allow_dirty:
            self.ensure_clean_git_repo() 
        return super().handle(*args, **options)

    def ensure_clean_git_repo(self):
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout:
            raise CommandError('Your git repository is not clean. Commit or stash your changes before running this command.')