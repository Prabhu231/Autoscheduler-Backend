from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import User
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError, PyJWTError
from django.conf import settings
from utils.password.change_password import change_password
import bcrypt

class Reset_Password_View(APIView):
    def post(self, request):
        
        from_app = request.data.get('app')
        if from_app:
            token = request.COOKIES.get('refresh_token')
            
        else:
            token = request.data.get('token', '')
        

        if not token:
            return Response({'error': 'This particular link is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,  
                algorithms=["HS256"]
            )
            user = User.objects.get(id=decoded_token['user_id'])

        except ExpiredSignatureError:
            return Response({'error': 'The password reset link has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        except DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        except PyJWTError as e:
            return Response({'error': 'Error decoding the token, please try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except User.DoesNotExist:
            return Response({'error': 'User with this ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        if not from_app:
            return change_password(user=user, password=request.data.get('password', ''))
        
        
        current_password = request.data.get('currentPassword')
        if not bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
            return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        return change_password(user=user, password=request.data.get('newPassword'))
