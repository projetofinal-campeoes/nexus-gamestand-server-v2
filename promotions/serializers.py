from rest_framework import serializers
from .models import Promotion
from rate_log.models import Rate_log
import ipdb


class PromotionSerializer(serializers.ModelSerializer):

    shiny_meter = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ["id", "name", "price", "promo_url", "description", "user_id", "shiny_meter"]
        read_only_fields = ["description"]

    
    def get_shiny_meter(self, instance: Rate_log):

        rates = Rate_log.objects.all()

        positive_like = 0
        negative_like = 0
        if len(rates) == 0:
            return 0

        for key, value in rates.like.items():
            if key:
                positive_like = key


    def create(self, validated_data: dict) -> Promotion:

        user_obj = validated_data.pop('user')

        return Promotion.objects.create(**validated_data, user_id=user_obj.id)


    def update(self, instance: Promotion, validated_data: dict) -> Promotion:

        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()

        return instance