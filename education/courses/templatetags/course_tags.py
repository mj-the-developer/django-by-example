from django import template
from django.db.models import Model


register = template.Library()


@register.filter
def model_name(obj: Model):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
