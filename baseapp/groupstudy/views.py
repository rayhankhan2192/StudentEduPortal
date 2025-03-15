from django.shortcuts import render
from .models import CreateGroup
from .serializers import CreateGroupSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CreateGroupApiView(APIView):
    def post(self, request):
        permission_classes = [IsAuthenticated]
        serializer = CreateGroupSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Group successfully created!'}, status=status.HTTP_200_OK)
        return Response({"message": 'Something went wrong. Try again!'}, status=status.HTTP_400_BAD_REQUEST)