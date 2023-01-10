from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Promotion
from rate_log.models import Rate_log
from rate_log.serializers import RateSerializer
from . serializers import PromotionSerializer
from .permissions import AccountOwner
from django.shortcuts import get_object_or_404

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


class PromotionsDetailsIdRate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AccountOwner]

    def post(self, request: Request, pk: str, rate: str) -> Response:
        
        new_rate = RateSerializer(data= request.data)

        new_rate.is_valid(raise_exception=True)

        new_rate.save(user=request.user, pk_promotion=pk, fk_rate=rate)

        if new_rate.data == {}:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(new_rate.data, status.HTTP_201_CREATED)
    

class RateViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AccountOwner]

    def get(self, request: Request) -> Response:

        rates = Rate_log.objects.all()

        rates_list = RateSerializer(rates, many=True)

        return Response(rates_list.data, status.HTTP_200_OK)
