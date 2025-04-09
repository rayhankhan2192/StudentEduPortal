from django.urls import path
from . import views

urlpatterns = [
    path('create-groupstudy/', views.CreateGroupApiView.as_view(), name='create-studygroup'),
    path('get-groupstudy/', views.GetStudyGroup.as_view(), name='get-studygroup'),
]