from .models import CustomGames
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomGamesSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .permissions import IsAccountOwner


class ListGameView(ListAPIView):
    queryset = CustomGames.objects.all()
    serializer_class = CustomGamesSerializer

class CreateGameView(CreateAPIView):
    queryset = CustomGames.objects.all()
    serializer_class = CustomGamesSerializer

    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user.id)

class RetrieveUpdateGameView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    
    queryset = CustomGames.objects.all()
    serializer_class = CustomGamesSerializer

    def perform_create(self, serializer):
        return serializer.save(game_id=self.kwargs[self.lookup_field])