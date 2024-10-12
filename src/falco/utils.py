import importlib.util
import subprocess
from contextlib import contextmanager

from rich.progress import Progress, SpinnerColumn, TextColumn

if importlib.util.find_spec("falco_cli"):
    from falco_cli.utils import run_html_formatters, run_python_formatters
else:
    def run_html_formatters(*_, **__):
        pass


    def run_python_formatters(*_, **__):
        pass


@contextmanager
def simple_progress(description: str, display_text="[progress.description]{task.description}"):
    progress = Progress(SpinnerColumn(), TextColumn(display_text), transient=True)
    progress.add_task(description=description, total=None)
    try:
        yield progress.start()
    finally:
        progress.stop()


def clean_git_repo() -> bool:
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=False) # noqa
    return result.stdout.strip() == ""
