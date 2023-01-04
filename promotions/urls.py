from django.urls import path

urlpatterns = [
    path("promotions/"),
    path('promotions/<int:promotion_id>/'),   
    path('promotions/<int:promotion_id>/<:rate>/'),
]