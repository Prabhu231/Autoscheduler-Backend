# views/auth/reset_password_request.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import User
from datetime import datetime, timedelta, timezone
from django.conf import settings
import jwt
from jwt.exceptions import PyJWTError
from utils.mail.send_reset_mail import send_password_reset_mail


class Forgot_Password_View(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Database error while retrieving user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            
            now = datetime.now(timezone.utc)

            expiration_time = now + timedelta(minutes=15)
            payload = {
                "user_id": user.id,
                "iat": int(now.timestamp()),
                "exp": int(expiration_time.timestamp()),  
                "type": "reset"
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        except PyJWTError:
            return Response({'error': 'Failed to generate reset token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': 'Unexpected error while generating token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            send_password_reset_mail(email=email, token=token)
        except Exception as e:
            return Response({'error': 'Failed to send password reset email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
