from django import template
from users.models import Follow
from django.shortcuts import redirect

register = template.Library()

@register.filter(name='is_following')
def is_following(requser, user):
    return Follow.objects.filter(following=user, follower=requser).exists()
