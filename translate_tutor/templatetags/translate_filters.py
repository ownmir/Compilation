from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def em_selections(word_or_two, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<em lang="translate">%s</em>' % esc(word_or_two)
    return mark_safe(result)