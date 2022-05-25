from django import template

register = template.Library()

@register.filter
def _url(iframe):
    data = iframe.split("https://")[1]
    return data


register.filter("_url", _url)