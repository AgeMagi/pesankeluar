from django import template

from .. import models

register = template.Library()


@register.inclusion_tag('departments/last_message.html')
def last_message():
    message = models.Message.objects.latest('id')
    return {'message': message}


@register.inclusion_tag('departments/five_last_message.html')
def five_last_message():
    messages = models.Message.objects.all().order_by(
        '-id'
    ).values(
        'nomor',
        'dep',
        'div',
        'name'
    )[:5]
    return {'messages': messages}