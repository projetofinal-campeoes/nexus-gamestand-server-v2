from rest_framework import serializers
from .models import Promotion


class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = ["id", "name", "price", "promo_urls", "description", "user_id"]
        read_only_fields = ["description"]

    def create(self, validated_data: dict) -> Promotion:
        return Promotion.objects.create(**validated_data)

    def update(self, instance: Promotion, validated_data: dict) -> Promotion:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()

        return instance