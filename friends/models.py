from django.db import models

import uuid


class Friend(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=32)
    friend_id = models.UUIDField(null=True, blank=True)
    friend_name = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="friends",
    )
