from django.shortcuts import render
from .models import GroupStudy
from .serializers import CreateGroupSerializers, GroupStudySerializer, GroupStudyMessageSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions, authentication
from django.db.models import Q


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

from django.shortcuts import get_object_or_404

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

