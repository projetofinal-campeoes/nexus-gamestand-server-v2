from .models import CustomGames
from rest_framework.views import View
from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: CustomGames) -> bool:
        if (
            (request.user.is_authenticated and request.user.is_superuser)
            or request.user.is_authenticated
            and request.user.id == obj.user_id
        ):
            return True

        return False