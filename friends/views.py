from rest_framework import generics
from rest_framework.views import Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import (
    UserExists,
    AddAccountOwner,
    AddAccountDuplicated,
    UserAddedExists,
    DeleteOwnAccount,
)

from .serializers import FriendSerializer
from .models import Friend


class FriendView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        UserExists,
        AddAccountOwner,
        AddAccountDuplicated,
    ]

    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)

    def perform_create(self, serializer: FriendSerializer) -> None:
        serializer.save(user=self.request.user)


class FriendDetailView(generics.RetrieveAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UserAddedExists, DeleteOwnAccount]

    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = Friend.objects.get(friend_id=self.kwargs[self.lookup_field])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = Friend.objects.filter(friend_id=self.kwargs[self.lookup_field])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
