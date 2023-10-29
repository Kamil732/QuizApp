from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_time_difference(obj):
    now = timezone.now()

    time_ago = now - obj

    days_ago = time_ago.days
    seconds_ago = time_ago.seconds

    hours_ago = seconds_ago//3600
    minutes_ago = (seconds_ago//60)%60

    if days_ago <= 0:
        if hours_ago <= 0:
            if minutes_ago <= 0:
                return 'just at the moment'
            return f'{minutes_ago} minutes ago'
        return f'{hours_ago} hours ago'
    elif days_ago == 1:
        return 'yesterday'
    return f'{days_ago} days ago'