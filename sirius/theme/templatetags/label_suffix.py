from django import template


register = template.Library()


@register.filter("set_label_suffix")
def set_label_suffix(field, suffix=''):
    field.field.label_suffix = suffix
    return field