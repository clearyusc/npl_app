import random

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(name='random_image')
def random_image():
    choices = ['npl/neighborhood-1.jpg','npl/neighborhood-2.jpg','npl/neighborhood-3.jpg']
    random_img = random.choice(choices)
    return '/npl/static/'+random_img