from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def addparams(url, params):
    if url.find('?') > -1:
        return url + '&' + params
    else:
        return url + '?' + params