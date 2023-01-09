from django.urls import path
from .views import PromotionsView, PromotionsDetailsId, PromotionsDetailsIdRate, RateViews

urlpatterns = [
    path("promotions/", PromotionsView.as_view()),
    path("rates/", RateViews.as_view()),
    path('promotions/<pk>/', PromotionsDetailsId.as_view()),   
    path('promotions/<pk>/<rate>', PromotionsDetailsIdRate.as_view()),
]