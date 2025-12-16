from django import template

register = template.Library()
@register.filter

def hi(obj):
    return "Hello, world!"