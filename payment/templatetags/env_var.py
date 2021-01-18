# import os
from getenv import env
from django import template


register = template.Library()


@register.simple_tag
def get_env_var(key):
    return env(key)
