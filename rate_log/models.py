from django.db import models
import uuid

class Rate_log(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    like = models.BooleanField()

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rate")
    promotion  = models.ForeignKey("promotions.Promotion", on_delete=models.CASCADE, related_name="rate")
