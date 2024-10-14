from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.http import QueryDict
from django.template import Context
from django.template import RequestContext
from django.template import Template
from model_bakery import baker

from django_twc_toolbox.templatetags.django_twc_toolbox import class_name
from django_twc_toolbox.templatetags.django_twc_toolbox import display_name
from django_twc_toolbox.templatetags.django_twc_toolbox import elided_page_range
from falco.templatetags.django_twc_toolbox import initials
from django_twc_toolbox.templatetags.django_twc_toolbox import klass
from django_twc_toolbox.templatetags.django_twc_toolbox import query_string
from django_twc_toolbox.templatetags.django_twc_toolbox import startswith

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.mark.parametrize(
    "model,kwargs,expected",
    [
        (User, {"username": "johndoe", "first_name": "John", "last_name": "Doe"}, "JD"),
        (User, {"username": "janedoe"}, "J"),
        (AnonymousUser, {}, "N/A"),
    ],
)
def test_initials(model, kwargs, expected):
    user = model(**kwargs)

    assert initials(user) == expected


@pytest.mark.parametrize(
    "model,kwargs,expected",
    [
        (User, {"username": "johndoe", "first_name": "John", "last_name": "Doe"}, "JD"),
        (User, {"username": "janedoe"}, "J"),
        (AnonymousUser, {}, "N/A"),
    ],
)
def test_initials_templatet_ag(model, kwargs, expected):
    if kwargs:
        user = baker.make(model, **kwargs)
    else:
        user = model()

    template = Template("{% load django_twc_toolbox %} Initials: {{ user|initials }}")

    rendered = template.render(Context({"user": user}))

    assert f"Initials: {expected}" in rendered


@pytest.mark.parametrize(
    "model,kwargs,expected",
    [
        (
            User,
            {"username": "johndoe", "first_name": "John", "last_name": "Doe"},
            "John Doe",
        ),
        (User, {"username": "janedoe", "first_name": "Jane"}, "Jane"),
        (User, {"username": "bobsmith"}, "Bobsmith"),
        (AnonymousUser, {}, "N/A"),
    ],
)
def test_display_name(model, kwargs, expected):
    user = model(**kwargs)

    assert display_name(user) == expected


@pytest.mark.parametrize(
    "model,kwargs,expected",
    [
        (
            User,
            {"username": "johndoe", "first_name": "John", "last_name": "Doe"},
            "John Doe",
        ),
        (User, {"username": "janedoe", "first_name": "Jane"}, "Jane"),
        (User, {"username": "bobsmith"}, "Bobsmith"),
        (AnonymousUser, {}, "N/A"),
    ],
)
def test_display_name_template_tag(model, kwargs, expected):
    if kwargs:
        user = baker.make(model, **kwargs)
    else:
        user = model()

    template = Template("{% load django_twc_toolbox %} Name: {{ user|display_name }}")

    rendered = template.render(Context({"user": user}))

    assert f"Name: {expected}" in rendered







