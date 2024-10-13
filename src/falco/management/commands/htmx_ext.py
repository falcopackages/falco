from pathlib import Path

import httpx
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from falco.management.commands.htmx import default_htmx_output_folder
from falco.management.commands.htmx import network_request_with_progress
from falco.utils import simple_progress
from rich import print as rich_print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

REGISTRY_URL = "https://htmx-extensions.oluwatobi.dev/extensions.json"


class Command(BaseCommand):
    help = "Download one of htmx extensions"

    def add_arguments(self, parser):
        parser.add_argument(
            "name",
            type=str,
            nargs="?",
            help="The name of the extension to download, if not specified will list all extensions",
            default=None,
        )
        parser.add_argument(
            "-o",
            "--output-dir",
            type=Path,
            default=None,
            help="The directory to write the downloaded file to.",
        )

    def handle(self, *_, **options):
        output_dir = options.get("output_dir") or default_htmx_output_folder()
        name = options.get("name")
        if name:
            self.download(name, output_dir=output_dir)
        else:
            self.list_all()

    def download(self, name: str, output_dir: Path):
        extensions = self.read_registry()
        extension = extensions.get(name)

        if not extension:
            msg = f"Could not find {name} extension."
            raise CommandError(msg)

        with simple_progress(f"Downloading {name} extension"):
            download_url = extension.get("download_url")
            response = httpx.get(download_url, follow_redirects=True)

            output_file = output_dir / f"{name}.js"
            output_file.write_text(response.text)

        rich_print(
            Panel(
                f"[green]Extension {name} downloaded successfully![/green]",
                subtitle=extension.get("doc_url"),
            )
        )

    def list_all(self):
        extensions = self.read_registry()
        table = Table(
            title="Htmx Extensions",
            caption="Full details at https://htmx-extensions.oluwatobi.dev",
            show_lines=True,
        )
        table.add_column("Name", style="green")
        table.add_column("Description", style="magenta")

        for name, metadata in extensions.items():
            table.add_row(name, metadata.get("description", ""))
        console = Console()
        console.print(table)

    @classmethod
    def read_registry(cls):
        with network_request_with_progress(REGISTRY_URL, "Loading extensions registry") as response:
            return response.json()
