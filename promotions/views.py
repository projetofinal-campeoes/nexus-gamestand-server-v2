from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import Promotion
from .serializers import PromotionSerializer

class PromotionsView(ListCreateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PromotionsDetailsId(RetrieveUpdateDestroyAPIView):
    ...


class PromotionsDetailsIdRate(CreateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def perform_create(self, serializer):
            serializer.save(rate=id)

