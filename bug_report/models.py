from django.db import models
import uuid

class PageChoices(models.TextChoices):
    LOGIN = 'Login'
    REGISTER = 'Register'
    HOME = 'Home'
    PROFILE = 'Profile'
    GAMES = 'Games'
    PROMOTIONS = 'Promotions'
    FRIENDS = 'Friends'
    SETTINGS = 'Settings'
    BUG_REPORT = 'Bug report'

class BugReport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    page = models.CharField(max_length=20, choices=PageChoices.choices, default=PageChoices.HOME)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bugs_report')