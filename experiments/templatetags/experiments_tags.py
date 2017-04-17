from django import template
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
import inspect

register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})

@register.filter(name='get')
def get(o, index):
    try:
        return getattr(o, index)
    except:
        pass
    try:
        print(o)
        return o[str(index)]
    except:
        pass
    return settings.TEMPLATE_STRING_IF_INVALID