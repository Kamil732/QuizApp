from django import template

register = template.Library()

@register.filter
def last_number_less(value):
    value = value.replace(value[-1], str(int(value[-1])-1))
    return value

@register.filter
def last_number_greater(value):
    value = value.replace(value[-1], str(int(value[-1])+1))
    return value

@register.filter
def last(value, number):
    return True if value[-1] == str(number) else False

@register.filter
def range_func(value):
    return range(value)