from . import views
from django.urls import path


urlpatterns = [
    path("custom_games/", views.ListGameView.as_view()),
    path("custom_games/create/", views.CreateGameView.as_view()),
    path("custom_games/<pk>/", views.RetrieveUpdateGameView.as_view()),
]