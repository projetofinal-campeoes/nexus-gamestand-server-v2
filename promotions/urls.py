from django.urls import path
from .views import PromotionsView, PromotionsDetailsId, PromotionsDetailsIdRate

urlpatterns = [
    path("promotions/", PromotionsView.as_view()),
    path('promotions/<pk>/', PromotionsDetailsId.as_view()),   
    path('promotions/<fk>/', PromotionsDetailsIdRate.as_view()),
]