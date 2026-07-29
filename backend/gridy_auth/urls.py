from gridy_auth.views import UserProfileView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, ResidentImportView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('me/', UserProfileView.as_view(), name='auth_me'),
    path('import-residents/', ResidentImportView.as_view(), name='import_residents'),
]
