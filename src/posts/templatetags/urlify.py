from urllib import quote_plus
from django import templates


register = temlate.Library()

@register.filter
def urllify(value):
    return quote_plus(value)
