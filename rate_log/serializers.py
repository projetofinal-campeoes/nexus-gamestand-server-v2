from rest_framework import serializers
from .models import Rate_log
from promotions.models import Promotion
import ipdb

class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate_log
        fields = ["id", "user_id", "like", "promotion_id"]
        read_only_fields = ["like"]


    def create(self, validated_data: dict) -> Rate_log:

        user_obj = validated_data.pop('user')
        promotion_id_kwargs = validated_data.pop('pk_promotion')
        rate = validated_data.pop('fk_rate')

        promotion_obj_rate = Promotion.objects.get(id=promotion_id_kwargs).rate

        for dict in promotion_obj_rate.values():

            if (dict["user_id"] == user_obj.id):

                if (dict["like"] == True) and (rate == "dislike"):
                    rate_obj = Rate_log.objects.get(id=dict["id"])
                    setattr(rate_obj, "like", False)
                    rate_obj.save()
                    return rate_obj

                if (dict["like"] == False) and (rate == "like"):
                    rate_obj = Rate_log.objects.get(id=dict["id"])
                    setattr(rate_obj, "like", True)
                    rate_obj.save()
                    return rate_obj
            
                if (dict["like"] == True) and (rate == "like"):
                    rate_obj = Rate_log.objects.get(id=dict["id"])
                    rate_obj.delete()
                    return {}

                if (dict["like"] == False) and (rate == "dislike"):
                    rate_obj = Rate_log.objects.get(id=dict["id"])
                    rate_obj.delete()
                    return {}
                
        if rate == "dislike":
            validated_data['like'] = False

        if rate == "like": 
            validated_data['like'] = True
                           
        return Rate_log.objects.create(**validated_data, user_id=user_obj.id, promotion_id=promotion_id_kwargs)
    
    
    def update(self, instance: Rate_log, validated_data: dict) -> Promotion:

        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()

        return instance

    
        
