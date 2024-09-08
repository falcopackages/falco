from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import FileResponse
from django.http import HttpRequest
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from falco.conf import app_settings
from falco.decorators import login_not_required


@require_GET
@cache_control(max_age=0 if settings.DEBUG else app_settings.CACHE_TIME_FAVICON, immutable=True, public=True)
@login_not_required
def favicon(request: HttpRequest) -> HttpResponse | FileResponse:
    name = request.path.lstrip("/")
    if path := finders.find(name):
        return FileResponse(Path(path).read_bytes())
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            '<text y=".9em" font-size="90">🚀</text>'
            "</svg>"
        ),
        content_type="image/svg+xml",
    )
