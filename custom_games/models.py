from django.db import models
import uuid

class CustomGames(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=23)
    image_url = models.TextField()
    platform = models.CharField(max_length=16)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="games",
    )
    class Meta:
        unique_together = ('name', 'platform')
