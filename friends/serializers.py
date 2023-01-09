from rest_framework import serializers
from .models import Friend
from users.models import User


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = [
            "id",
            "username",
            "friend_id",
            "friend_name",
            "user_id",
        ]
        read_only_fields = (
            "user_id",
            "friend_id",
            "friend_name",
        )
        extra_kwargs = {
            "username": {"write_only": True},
        }

    def create(self, validated_data: dict) -> Friend:
        username = validated_data.pop("username")

        friend = User.objects.get(username=username)

        validated_data["friend_id"] = friend.id
        validated_data["friend_name"] = friend.username
        return Friend.objects.create(**validated_data)
