from rest_framework import serializers
from .models import Promotion
from rate_log.models import Rate_log
import ipdb


class PromotionSerializer(serializers.ModelSerializer):

    shiny_meter = serializers.SerializerMethodField()
    shiny_quant = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ["id", "name", "price", "promo_url", "description", "user_id", "shiny_meter", "shiny_quant"]
        read_only_fields = ["description"]

    
    def get_shiny_quant(self, instance: Rate_log):

        promotion_obj = Promotion.objects.all()

        count = 0
        for dict_promo in promotion_obj:
            for dict in dict_promo.rate.values():
                count += 1

        return count

    
    def get_shiny_meter(self, instance: Rate_log):

        rates = Rate_log.objects.all()

        positive_like = 0
        negative_like = 0

        if len(rates) == 0:
            return 0

        for dict in rates:
            if dict.like:
                positive_like += 1
            else:
                negative_like += 1
        
        return positive_like - negative_like


    def create(self, validated_data: dict) -> Promotion:

        user_obj = validated_data.pop('user')

        return Promotion.objects.create(**validated_data, user_id=user_obj.id)


    def update(self, instance: Promotion, validated_data: dict) -> Promotion:

        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()

        return instance