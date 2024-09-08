from django.urls import path

from .views import favicon

urlpatterns = [
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
