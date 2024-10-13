from django.urls import path
from django.views import defaults as default_views

from .views import favicon

favicon_urlpatterns = [
    path("android-chrome-192x192.png", favicon),
    path("android-chrome-512x512.png", favicon),
    path("apple-touch-icon.png", favicon),
    path("browserconfig.xml", favicon),
    path("favicon-16x16.png", favicon),
    path("favicon-32x32.png", favicon),
    path("favicon.ico", favicon),
    path("mstile-150x150.png", favicon),
    path("safari-pinned-tab.svg", favicon),
]


errors_urlpatterns = [
    path(
        "400/",
        default_views.bad_request,
        kwargs={"exception": Exception("Bad Request!")},
    ),
    path(
        "403/",
        default_views.permission_denied,
        kwargs={"exception": Exception("Permission Denied")},
    ),
    path(
        "404/",
        default_views.page_not_found,
        kwargs={"exception": Exception("Page not Found")},
    ),
    path("500/", default_views.server_error),
]
