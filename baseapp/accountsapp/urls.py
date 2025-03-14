from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegistrationApiView.as_view(), name='signup'),
    path('create-user/',views.UserCreateApiView.as_view(), name='create-user'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend-otp'),
    
]