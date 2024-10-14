from __future__ import annotations

import sys
from dataclasses import dataclass

from django.conf import settings

if sys.version_info >= (3, 12):
    from typing import override
else:  # pragma: no cover
    from typing_extensions import override  # pyright: ignore[reportUnreachable]


FALCO_SETTINGS_NAME = "FALCO"


@dataclass(frozen=True)
class AppSettings:
    CACHE_TIME_FAVICON = 60 * 60 * 24  # one day
    CACHE_TIME_ROBOTS_TXT = 60 * 60 * 24  # one day
    CACHE_TIME_SECURITY_TXT = 60 * 60 * 24  # one day
    TEMPLATE_ROBOTS_TXT = "robots.txt"
    TEMPLATE_SECURITY_TXT = ".well-known/security.txt"
    DEFAULT_PAGE_SIZE = 20
    SENTRY_DISGARDED_METHODS = ["GET", "HEAD"]
    SENTRY_DISGARDED_PATHS = ["/health/"]
    SENTRY_PROFILE_RATE = 0.5
    SENTRY_TRACES_RATE = 0.5
    WORK = {}

    @override
    def __getattribute__(self, __name: str) -> object:
        user_settings = getattr(settings, FALCO_SETTINGS_NAME, {})
        return user_settings.get(__name.lower(), super().__getattribute__(__name))  # pyright: ignore[reportAny]


app_settings = AppSettings()
