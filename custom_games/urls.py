from django.urls import path
from . import views

urlpatterns = [
    path("custom_games/", views.ListCreateAPIView.as_view()),
    path("custom_games/<int:pk>/", views.RetrieveUpdateDestroyAPIView.as_view()),
]
