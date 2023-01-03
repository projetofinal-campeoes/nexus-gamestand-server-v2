from .models import CustomGames
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomGamesSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class ListCreateAPIView(ListCreateAPIView):
    queryset = CustomGames.objects.all()
    serializer_class = CustomGamesSerializer

class RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = CustomGames.objects.all()
    serializer_class = CustomGamesSerializer

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user.id)