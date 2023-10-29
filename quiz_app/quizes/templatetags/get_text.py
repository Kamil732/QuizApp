from django import template

register = template.Library()

@register.filter
def get(value, letters):
    if letters >= len(value):
        return value
    return str(value[:letters]) + '...'