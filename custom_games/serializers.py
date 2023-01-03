from rest_framework import serializers
from .models import CustomGames


class CustomGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGames
        fields = ('id', 'name', 'image_url', 'platform')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        return CustomGames.objects.create(**validated_data)

    def update(self, instance: CustomGames, validated_data: dict) -> CustomGames:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance