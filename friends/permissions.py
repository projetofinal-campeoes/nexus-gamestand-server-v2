from rest_framework import permissions
from rest_framework.views import Request, View
from django.http import Http404
from rest_framework.exceptions import ValidationError

from .models import Friend
from users.models import User

from rest_framework.exceptions import APIException
from rest_framework import status


class GenericAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class UserExists(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True

        friend = User.objects.filter(username=req.data["username"])

        if friend:
            return True
        raise GenericAPIException(
            detail={"detail": "User not found."},
            status_code=404,
        )


class AddAccountOwner(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True

        if not req.data["username"] == req.user.username:
            return True
        raise GenericAPIException(
            detail={"detail": "Not able to add own account."},
            status_code=400,
        )


class AddAccountDuplicated(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True

        friend = Friend.objects.filter(friend_name=req.data["username"])

        if not friend:
            return True
        raise GenericAPIException(
            detail={"detail": "User already added."},
            status_code=400,
        )


class UserAddedExists(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "DELETE":
            return True

        friend = Friend.objects.filter(friend_id=view.kwargs["pk"])

        if friend:
            return True
        raise GenericAPIException(
            detail={"detail": "This user is not added."},
            status_code=404,
        )


class DeleteOwnAccount(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True

        friend = Friend.objects.filter(friend_id=view.kwargs["pk"])

        if friend:
            return True
        raise GenericAPIException(
            detail={"detail": "User not Found."},
            status_code=404,
        )
