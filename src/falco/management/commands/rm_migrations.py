from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from falco.management.base import GitAwareBaseCommand
from django.apps import apps

class Command(GitAwareBaseCommand):
    help = 'Remove all migrations for the specified applications directory, intended only for development.'

    def add_arguments(self, parser):
        parser.add_argument(
            'appname',
            type=str,
            nargs='*',
            help='The name of the app to remove migrations for.'
        )


    def handle(self, *args, **options):
        app_names = options['appname']
        if not settings.DEBUG:
            raise CommandError('This command can only be run with DEBUG=True.')

        if not app_names:
            apps_dir = getattr(settings, 'APPS_DIR', None)
            if not apps_dir:
                self.stdout.write(self.style.ERROR('You must specify an app name or set APPS_DIR.'))
                return
            apps_dirs = list(apps_dir.iterdir())
        else:
            apps_dirs = []
            for app_name in app_names:
                try:
                    app_config = apps.get_app_config(app_name)
                    apps_dirs.append(Path(app_config.path))
                except LookupError:
                    self.stdout.write(self.style.ERROR(f'App "{app_name}" not found.'))
                    return

        processed_apps = set()
        for folder in apps_dirs:
            migration_dir = folder / 'migrations'
            if not migration_dir.exists():
                continue
            processed_apps.add(folder.stem)
            for file in migration_dir.iterdir():
                if file.suffix == '.py' and file.name != '__init__.py':
                    file.unlink()

        if processed_apps:
            self.stdout.write(self.style.SUCCESS(f'Removed migration files for apps: {", ".join(processed_apps)}'))
        else:
            self.stdout.write(self.style.WARNING('No migration files were found to remove.'))
