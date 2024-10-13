import importlib.util

from django.contrib.auth.models import User
from django.http import HttpRequest as HttpRequestBase

if importlib.util.find_spec("django_htmx"):
    # TODO: should look for the middleware, not the package
    from django_htmx.middleware import HtmxDetails

    class HttpRequest(HttpRequestBase):
        htmx: HtmxDetails

else:

    class HttpRequest(HttpRequestBase):
        pass


class AuthenticatedHttpRequest(HttpRequest):
    user: User
