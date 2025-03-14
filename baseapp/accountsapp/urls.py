from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegistrationApiView.as_view(), name='signup'),
    
]