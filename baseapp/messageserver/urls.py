from django.urls import path
from . import views

urlpatterns = [
    path('create-group/', views.CreateGroupView.as_view(), name='create-group'),
    path('groups/join/', views.JoinGroupView.as_view(), name='join-group'),
    path('groups/list/', views.GroupListView.as_view(), name='group-list'),
]