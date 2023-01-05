from django.urls import path
from .views import PromotionsView, PromotionsDetailsId, PromotionsDetailsIdRate

urlpatterns = [
    path("promotions/", PromotionsView.as_view()),
    path('promotions/<str:promotion_id>/', PromotionsDetailsId.as_view()),   
    path('promotions/<str:promotion_id>/<int:rate>/', PromotionsDetailsIdRate.as_view()),
]