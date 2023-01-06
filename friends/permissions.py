from rest_framework import permissions
from rest_framework.views import Request, View
from rest_framework.exceptions import ValidationError

from .models import Friend
from users.models import User


class UserExists(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True

        friend = User.objects.filter(username=req.data["username"])

        if friend:
            return True
        raise ValidationError(
            detail={"detail": "User not found"},
            code=404,
        )


class AddAccountOwner(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True

        if not req.data["username"] == req.user.username:
            return True
        raise ValidationError(
            detail={"detail": "Not able to add own account."},
            code=400,
        )


class AddAccountDuplicated(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True

        friend = Friend.objects.filter(friend_name=req.data["username"])

        if not friend:
            return True
        raise ValidationError(
            detail={"detail": "User already added."},
            code=400,
        )


class UserAddedExists(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "DELETE":
            return True

        friend = Friend.objects.filter(friend_id=view.kwargs["pk"])

        if friend:
            return True
        raise ValidationError(
            detail={"detail": "This user is not added."},
            code=400,
        )


class DeleteOwnAccount(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True

        friend = Friend.objects.filter(friend_id=view.kwargs["pk"])

        if friend:
            return True
        raise ValidationError(
            detail={"detail": "User not Found."},
            code=404,
        )
