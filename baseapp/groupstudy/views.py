from django.shortcuts import render
from .models import GroupStudy
from .serializers import CreateGroupSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions, authentication

class CreateGroupApiView(APIView):
    def post(self, request):
        authentication_classes = [JWTAuthentication]
        permission_classes = [permissions.IsAuthenticated] 
        serializer = CreateGroupSerializers(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Group successfully created!'}, status=status.HTTP_200_OK)
        return Response({"message": 'Something went wrong. Try again!'}, status=status.HTTP_400_BAD_REQUEST)

class GetStudyGroupList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    
    def get(self, request):
        group = GroupStudy.objects.filter(auth_users = request.user)
        serializer = CreateGroupSerializers(group, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            