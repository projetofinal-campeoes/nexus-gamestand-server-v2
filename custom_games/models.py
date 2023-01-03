from django.db import models

class CustomGames(models.Model):
    name = models.CharField(max_length=23)
    image_url = models.TextField()
    platform = models.CharField(max_length=16)

"""     user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="custom_games",
    ) """
