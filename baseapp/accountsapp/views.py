from django.shortcuts import render
from .models import Account
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RegistrationApiView(APIView):
    def post(self, request):
        data = request.data
        serilizers = RegistrationSerializer(data = data)
        if serilizers.is_valid():
            serilizers.save()
            return Response({"message": 'Successfuly Registered!'}, status=status.HTTP_201_CREATED)
        return Response({"message": 'Something went wrong, Try again!'}, status=status.HTTP_400_BAD_REQUEST)
