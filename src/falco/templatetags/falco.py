from django import template

register = template.Library()


@register.filter()
def lookup(value):
    lookup_field = getattr(value, "lookup_field", "pk")
    return getattr(value, lookup_field)


@register.filter()
def field_verbose_names(objects, fields):
    return [objects[0]._meta.get_field(f).verbose_name for f in fields]  # noqa


@register.filter(name="getattr")
def get_attribute(obj, field):
    return getattr(obj, field)


@register.filter()
def field_class_name(obj, field):
    return obj._meta.get_field(field).__class__.__name__  # noqa
