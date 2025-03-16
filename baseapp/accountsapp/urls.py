from django.urls import path
from . import views

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('signup/', views.RegistrationApiView.as_view(), name='signup'),
    path('create-user/',views.UserCreateApiView.as_view(), name='create-user'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend-otp'),

    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]