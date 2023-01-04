from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=32, unique=True)
    avatar_url = models.TextField(blank=True)
    email = models.EmailField(max_length=128, unique=True)
    status = models.BooleanField(default=True)
    steam_user = models.CharField(max_length=32)
    gamepass = models.BooleanField(default=False)
