from typing import TypeVar

from django import template
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser
from django.db import models

register = template.Library()

_TModel = TypeVar("_TModel", bound=models.Model)


@register.filter()
def lookup(obj: _TModel) -> str:
    lookup_field = getattr(obj, "lookup_field", "pk")
    return str(getattr(obj, lookup_field))


@register.filter()
def field_verbose_names(objects, fields) -> list[str]:
    return [objects[0]._meta.get_field(f).verbose_name for f in fields]  # noqa


@register.filter(name="getattr")
def get_attribute(obj: object, field: str):
    return getattr(obj, field)


@register.filter()
def field_class_name(obj: _TModel, field: str) -> str:
    return obj._meta.get_field(field).__class__.__name__  # noqa


@register.filter
def display_name(user: AbstractUser) -> str:
    if not hasattr(user, "username") or isinstance(user, AnonymousUser):
        return "N/A"

    if user.first_name and user.last_name:
        display_name_ = f"{user.first_name} {user.last_name}"
    elif user.first_name:
        display_name_ = user.first_name
    else:
        display_name_ = user.username

    return display_name_.title()


@register.filter
def initials(user: AbstractUser) -> str:
    if not hasattr(user, "username") or isinstance(user, AnonymousUser):
        return "N/A"

    initials_ = user.username[0].upper()

    if user.first_name and user.last_name:
        initials_ = f"{user.first_name[0].upper()}{user.last_name[0].upper()}"

    return initials_


@register.filter
def class_name(instance: object) -> str:
    return instance.__class__.__name__
