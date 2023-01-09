from .models import CustomGames
from rest_framework import serializers


class CustomGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGames
        fields = ('id', 'name', 'image_url', 'platform', 'user_id')
        unique_together = ('name', 'platform')
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
        }

    def create(self, validated_data):
        return CustomGames.objects.create(**validated_data)

    def update(self, instance: CustomGames, validated_data: dict) -> CustomGames:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance