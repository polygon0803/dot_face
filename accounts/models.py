from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dot_art = models.CharField(max_length=225, blank=True, null=True) # 15x15 = 225 characters (0 or 1)
    bio = models.TextField(blank=True, null=True)
    hobbies = models.CharField(max_length=255, blank=True, null=True)
    favorite_things = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username + "'s profile"

class DotArtEntry(models.Model):
    dot_art_string = models.CharField(max_length=225, unique=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"Dot Art: {self.dot_art_string[:10]}... ({self.votes} votes)"