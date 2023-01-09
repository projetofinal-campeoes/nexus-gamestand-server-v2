from rest_framework import permissions
from rest_framework.views import Request, View
from .views import User


class AccountOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        if (
            (request.user.is_authenticated and request.user.is_superuser)
            or request.user.is_authenticated
            and request.user == obj
        ):
            return True

        return False
