from rest_framework import serializers
from .models import Promotion


class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = ["id", "name", "price", "promo_urls", "description", "shiny_meter", "user"]
        read_only_fields = ["description", "shiny_meter"]

    def create(self, validated_data: dict) -> Promotion:
        ...

    def update(self, instance: Promotion, validated_data: dict) -> Promotion:
        ...