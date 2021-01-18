from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=264, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    website = models.URLField(max_length=128, blank=True, null=True)
    profilepicture = models.ImageField(upload_to='profile_picture', default='no_avatar.png', blank=True)
    background_img = models.ImageField(upload_to='profile_background', default='no_avatar.png', blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('useroverview', kwargs={
            'username': self.username
        })


class Follow(models.Model):
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower', on_delete=models.CASCADE)
