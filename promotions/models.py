from django.db import models
import uuid

class Promotion(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    promo_url = models.TextField(null=False, blank=False)
    description = models.CharField(max_length=256)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="promotions")