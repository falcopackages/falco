from django import template

register = template.Library()


@register.filter()
def lookup(value):
    lookup_field = getattr(value, "lookup_field", "pk")
    return getattr(value, lookup_field)


@register.filter()
def field_verbose_names(objects, fields):
    return [objects[0]._meta.get_field(f).verbose_name for f in fields] # noqa


@register.filter()
def object_value(obj, field):
    return getattr(obj, field, "")
