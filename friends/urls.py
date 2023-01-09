from django.urls import path
from . import views

urlpatterns = [
    path("friends/", views.FriendView.as_view()),
    path("friends/<pk>/", views.FriendDetailView.as_view()),
]
