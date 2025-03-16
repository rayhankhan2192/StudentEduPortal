from django.urls import path
from . import views

urlpatterns = [
    path('create-groupstudy/', views.CreateGroupApiView.as_view(), name='register'),
]