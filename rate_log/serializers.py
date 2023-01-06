from rest_framework import serializers
from .models import Rate_log
import ipdb

class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate_log
        fields = ["uuid", "user_id", "like", "promotion_id"]


    def create(self, validated_data: dict) -> Rate_log:

        ipdb.set_trace()

        user_obj = validated_data.pop('user')
        promotion_obj = validated_data.pop('promotion')

        return Rate_log.objects.create(**validated_data, user_id=user_obj, promotion_id=promotion_obj.id)