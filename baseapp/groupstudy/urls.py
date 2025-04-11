from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-groupstudy/', views.CreateGroupApiView.as_view(), name='create-studygroup'),
    path('join-groupstudy/', views.JoinStudyGroup.as_view(), name='join-studygroup'),
    path('get-groupstudy/', views.GetStudyGroupList.as_view(), name='get-studygroup'),
    path('join-studygroup/list/', views.JoinStudyGroupList.as_view(), name='join-study-group-list'),
    path('join-studygroup/list-all/', views.StudyGroupsAPIView.as_view(), name='join-study-group-list'),
    path('join-studygroup/<int:group_id>/', views.GetGroupByIdAPIViews.as_view(), name='get-group-by-id'),
    
    path('sendmessage/', views.SendMessageView.as_view(), name='sendMessage'),
    path('sendFile/', views.SendFileMessageView.as_view(), name='sendFile'),
    path('group/<int:group_id>/messages/', views.GetMessageView.as_view(), name='get_group_messages'),
]

if settings.DEBUG:
    urlpatterns += static('media/', document_root=settings.MEDIA_ROOT)