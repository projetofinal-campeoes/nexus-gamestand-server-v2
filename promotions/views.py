from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Promotion
from rate_log.models import Rate_log
from rate_log.serializers import RateSerializer
from . serializers import PromotionSerializer
from .permissions import AccountOwner
import ipdb

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
    queryset = Rate_log.objects.all()
    serializer_class = RateSerializer

    def perform_create(self, serializer):
            ipdb.set_trace()
            serializer.save(user=self.request.user.id)

