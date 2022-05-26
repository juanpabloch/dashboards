from django import template
from django.core import serializers

register = template.Library()

@register.filter
def _url(iframe):
    data = iframe.split("https://")[1]
    return data


@register.filter
def toJson(query):
    """convierte un query set a json"""
    data = serializers.serialize('json', query)
    return data


register.filter("_url", _url)
register.filter("toJson", toJson)