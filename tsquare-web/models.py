from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    github_access_token = models.CharField(max_length=255)
    gdrive_access_token = models.CharField(max_length=255)
    current_course = models.CharField(max_length=255)
