from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from falco.conf import app_settings
from falco.decorators import login_not_required

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

@require_GET
@cache_control(max_age=0 if settings.DEBUG else app_settings.CACHE_TIME_ROBOTS_TXT, immutable=True, public=True)
@login_not_required
def robots_txt(request: HttpRequest) -> HttpResponse:
    return render(request, app_settings.TEMPLATE_ROBOTS_TXT, content_type="text/plain")


@require_GET
@cache_control(max_age=0 if settings.DEBUG else app_settings.CACHE_TIME_SECURITY_TXT, immutable=True, public=True)
@login_not_required
def security_txt(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        app_settings.TEMPLATE_SECURITY_TXT,
        context={
            "year": timezone.now().year + 1,
        },
        content_type="text/plain",
    )
