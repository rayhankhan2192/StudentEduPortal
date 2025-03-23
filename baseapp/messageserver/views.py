from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserGroup, Message
from .serializer import GroupSerializer, MessageSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions, authentication

class CreateGroupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
        
    def post(self, request):
        serializers = GroupSerializer(data=request.data, context={'request': request})
        if serializers.is_valid():
            serializers.save()
            print(serializers.data)
            return Response({"message": 'Group successfully created!'}, status=status.HTTP_200_OK)
        print("Serializer Errors:", serializers.errors)
        return Response({"message": 'Something went wrong. Try again!'}, status=status.HTTP_400_BAD_REQUEST)

class JoinGroupView(APIView):
    def post(self, request):
        invite_code = request.data.get("invite_code")
        group = UserGroup.objects.filter(invite_code=invite_code).first()
        
        if group:
            if request.user in group.members.all():
                return Response({"message": "Already joined."}, status=status.HTTP_400_BAD_REQUEST)
            group.members.add(request.user)
            return Response({"message": "Joined successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid invite code"}, status=status.HTTP_400_BAD_REQUEST)

# Get all groups user joined
class GroupListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = UserGroup.objects.filter(members=request.user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#send a message to a group
class SendMessageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(sender = request.user)
            return Response({"message": "Message sent"}, status=status.HTTP_200_OK)
        return Response({"message": "Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST)
    
# Get all messages in a group
class GroupMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        messages = Message.objects.filter(group_id=group_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)