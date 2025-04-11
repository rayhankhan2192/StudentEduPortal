from django.shortcuts import render
from .models import GroupStudy, GroupStudyMessage
from .serializers import CreateGroupSerializers, GroupStudySerializer, GroupStudyMessageSerializer, GroupStudySendFileSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions, authentication
from django.db.models import Q
from django.http import FileResponse, Http404
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404

class CreateGroupApiView(APIView):
    def post(self, request):
        authentication_classes = [JWTAuthentication]
        permission_classes = [permissions.IsAuthenticated] 
        serializer = CreateGroupSerializers(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Group successfully created!'}, status=status.HTTP_200_OK)
        return Response({"message": 'Something went wrong. Try again!'}, status=status.HTTP_400_BAD_REQUEST)


class JoinStudyGroup(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    
    def post(self, request):
        invite_code = request.data.get("invite_code")
        group = GroupStudy.objects.filter(invite_code = invite_code).first()
        
        if group:
            if request.user in group.members.all():
                return Response({"message": "Already joined."}, status=status.HTTP_400_BAD_REQUEST)
            group.members.add(request.user)
            return Response({"message": "Joined successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid invite code"}, status=status.HTTP_400_BAD_REQUEST)


class JoinStudyGroupList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    def get(self, request):
        group = GroupStudy.objects.filter(members = request.user)
        serializer = CreateGroupSerializers(group, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetStudyGroupList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    def get(self, request):
        group = GroupStudy.objects.filter(auth_users = request.user)
        serializer = CreateGroupSerializers(group, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StudyGroupsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        groups = GroupStudy.objects.filter(
            Q(auth_users=user) | Q(members=user)
        ).distinct().order_by('-last_message_time', '-updated_at')
        serializer = GroupStudySerializer(groups, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetGroupByIdAPIViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id):
        user = request.user
        group = GroupStudy.objects.filter(
            Q(id=group_id) & (Q(auth_users=user) | Q(members=user))
        ).distinct().first()

        if group:
            serializer = GroupStudySerializer(group, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Group not found or access denied."}, status=status.HTTP_404_NOT_FOUND)


# class SendMessageView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self, request):
#         serializer = GroupStudyMessageSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save(sender = request.user)
#             return Response({"message": "Message sent to the Group"}, status=status.HTTP_200_OK)
#         return Response({"message": "Something went wrong to send message!"}, status=status.HTTP_400_BAD_REQUEST)


class SendMessageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        group_id = request.data.get('group')
        if not group_id:
            return Response({"message": "Group ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        group = get_object_or_404(GroupStudy, id=group_id)
        if request.user not in group.members.all():
            return Response({"message": "You are not a member of this group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = GroupStudyMessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response({"message": "Message sent to the Group"}, status=status.HTTP_200_OK)
        return Response({"message": "Something went wrong to send message!"}, status=status.HTTP_400_BAD_REQUEST)


class SendFileMessageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    # def post(self, request):
    #     group_id = request.data.get('group')
    #     if not group_id:
    #         return Response({"message": "Group ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    #     group = get_object_or_404(GroupStudy, id=group_id)
    #     if request.user not in group.members.all():
    #         return Response({"message": "You are not a member of this group."}, status=status.HTTP_403_FORBIDDEN)
    #     serializer = GroupStudySendFileSerializers(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save(sender=request.user)
    #         return Response({"message": "Message sent to the Group"}, status=status.HTTP_200_OK)
    #     return Response({"message": "Something went wrong to send message!"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        # Get the data from the request
        group_id = request.data.get('group')
        sender_id = request.data.get('sender')
        file = request.FILES.get('file')
        if not group_id or not sender_id or not file:
            return Response({'error': 'Missing group, sender, or file'}, status=status.HTTP_400_BAD_REQUEST)
        message = GroupStudyMessage.objects.create(
            group_id=group_id,
            sender_id=sender_id,
            file=file)
        return Response({
            'message': 'File uploaded successfully!',
            'file_url': message.file.url,
            'sender': message.sender.username,
            'group_id': message.group.id
        }, status=status.HTTP_201_CREATED)


class GetMessageView(ListAPIView):
    serializer_class = GroupStudyMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(GroupStudy, id=group_id)
        user = self.request.user
        if user != group.auth_users and user not in group.members.all():
            return GroupStudyMessage.objects.none()
        return group.messages.all().order_by('timestamp')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists() and self.request.user != get_object_or_404(GroupStudy, id=kwargs.get('group_id')).auth_users and self.request.user not in get_object_or_404(GroupStudy, id=kwargs.get('group_id')).members.all():
            return Response({"message": "You are not a member of this group."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)