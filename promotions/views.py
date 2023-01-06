from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Promotion
from . serializers import PromotionSerializer
from .permissions import AccountOwner

class PromotionsView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AccountOwner]

    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PromotionsDetailsId(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AccountOwner]

    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PromotionsDetailsIdRate(CreateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def perform_create(self, serializer):
            serializer.save(rate=id)

