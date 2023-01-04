from django.db import models


class Promotions(models.Model):

    class Meta:
        ordering = ["id"]

    name = models.CharField(max_length=64, null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    promo_url = models.TextField(null=False, blank=False)
    description = models.CharField(max_length=256)
    shiny_meter = models.IntegerField(default=0)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="promotions")