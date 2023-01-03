from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views

urlpatterns = [
       
    path("users/login/", jwt_views.TokenObtainPairView.as_view()),
    
    path('docs/', SpectacularAPIView.as_view(), name='schema'),   
    path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]