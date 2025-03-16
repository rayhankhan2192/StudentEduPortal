from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Group, Message
from .serializers import GroupSerializer, MessageSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions, authentication

class CreateGroupView(APIView):
    def post(self, request):
        authentication_classes = [JWTAuthentication]
        permission_classes = [permissions.IsAuthenticated]
        serializer = GroupSerializer(data = request.data, context = {"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Group successfully created!'}, status=status.HTTP_200_OK)
        return Response({"message": 'Something went wrong. Try again!'}, status=status.HTTP_400_BAD_REQUEST)

class JoinGroupView(APIView):
    def post(self, request):
        invite_code = request.data.get("invite_code")
        group = Group.objects.filter(invite_code=invite_code).first()
        
        if group:
            group.members.add(request.user)
            return Response({"message": "Joined successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid invite code"}, status=status.HTTP_400_BAD_REQUEST)