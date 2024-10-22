from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from falco.utils import simple_progress
from httpx import codes

HTMX_DOWNLOAD_URL = "https://unpkg.com/htmx.org@{version}/dist/htmx.js"
HTMX_GH_RELEASE_LATEST_URL = "https://api.github.com/repos/bigskysoftware/htmx/releases/latest"


class Command(BaseCommand):
    help = "Download the latest version (if no version is specified) of htmx."

    def add_arguments(self, parser):
        parser.add_argument("version", type=str, default="latest")
        parser.add_argument(
            "-o",
            "--output-dir",
            type=Path,
            default=None,
            help="The directory to write the downloaded file to.",
        )

    def handle(self, *_, **options):
        version = options["version"]
        version = version if version != "latest" else get_latest_tag()
        output_dir = options.get("output_dir") or default_htmx_output_folder()
        url = HTMX_DOWNLOAD_URL.format(version=version)

        with network_request_with_progress(url, f"Downloading htmx version {version}") as response:
            content = response.content.decode("utf-8")
            if response.status_code == codes.NOT_FOUND:
                msg = f"Could not find htmx version {version}."
                raise CommandError(msg)

        filepath = output_dir / "htmx.js"
        filepath.write_text(f"/*htmx@{version}*/{content}")
        self.stdout.write(
            self.style.SUCCESS(
                f"htmx version {version} downloaded successfully to {filepath}",
            )
        )


def get_latest_tag() -> str:
    with network_request_with_progress(HTMX_GH_RELEASE_LATEST_URL, "Getting htmx latest version") as response:
        try:
            return response.json()["tag_name"][1:]
        except KeyError as e:
            msg = (
                "Unable to retrieve the latest version of htmx. "
                "This issue may be due to reaching the GitHub API rate limit. Please try again later."
            )
            raise CommandError(msg) from e


def default_htmx_output_folder() -> Path:
    try:
        folder = Path(settings.STATICFILES_DIRS[0]) / "vendors" / "htmx"
    except IndexError:
        msg = "Add at least one folder in your STATICFILES_DIRS settings and make sure it exists"
        raise CommandError(msg)
    folder.mkdir(exist_ok=True, parents=True)
    return folder


@contextmanager
def network_request_with_progress(url: str, description: str):
    try:
        with simple_progress(description):
            yield httpx.get(url)
    except httpx.ConnectError as e:
        msg = f"Connection error, {url} is not reachable."
        raise CommandError(msg) from e
