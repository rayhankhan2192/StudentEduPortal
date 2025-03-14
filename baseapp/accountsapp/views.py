from django.shortcuts import render
from .models import Account, OTP
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.core.mail import send_mail


class RegistrationApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data = data, context={'request': request})
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    
                    otp_code = get_random_string(length=6, allowed_chars='1234567890')
                    OTP.objects.create(user=user, otp_code = otp_code)
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is {otp_code}. It will expire in 90 seconds.',
                        '',
                        [user.email],
                        fail_silently=False,
                    )
                    return Response({'message': 'An OTP has been sent to email. Please verified!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Roll back transaction if email sending fails or any error occurs
                return Response({'message': 'Registration failed. Please try again later.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
