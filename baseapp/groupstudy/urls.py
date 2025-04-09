from django.urls import path
from . import views

urlpatterns = [
    path('create-groupstudy/', views.CreateGroupApiView.as_view(), name='create-studygroup'),
    path('get-groupstudy/', views.GetStudyGroupList.as_view(), name='get-studygroup'),
    path('join-groupstudy/', views.JoinStudyGroup.as_view(), name='join-studygroup'),
    path('join-studygroup/list/', views.JoinStudyGroupList.as_view(), name='join-study-group-list'),
]