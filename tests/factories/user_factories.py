from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

User: AbstractUser = get_user_model()


def create_user_with_token(user_data=None) -> tuple[AbstractUser, RefreshToken]:
    if not user_data:
        user_data = {
            "username": "nexus_teste",
            "email": "nexus_teste@nexus.com",           
            "password": "654321",
        }

    user = User.objects.create_superuser(**user_data)
    user_token = RefreshToken.for_user(user)

    return user, user_token

def create_user_with_token_no_admin(user_data=None) -> tuple[AbstractUser, RefreshToken]:
    if not user_data:
        user_data = {
            "username": "nexus_teste_no_admin",
            "email": "nexus_teste_no_admin@nexus.com",           
            "password": "654321",
        }

    user = User.objects.create_user(**user_data)
    user_token = RefreshToken.for_user(user)

    return user, user_token