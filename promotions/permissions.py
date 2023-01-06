from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User
import ipdb


class AccountOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user