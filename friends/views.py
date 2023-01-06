from rest_framework import generics
from rest_framework.views import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import FriendSerializer
from .models import Friend


class FriendView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def perform_create(self, serializer: FriendSerializer) -> None:
        if self.request.data["username"] == self.request.user.username:
            return Response("Not able to add the own user.")

        serializer.save(user=self.request.user)


class FriendDetailView(generics.ListAPIView, generics.DestroyAPIView):
    ...
