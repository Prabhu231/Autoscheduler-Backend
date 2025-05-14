# email_scheduler/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError, PyJWTError
from django.conf import settings
from app.models import User
from utils.mail.send_mail import send as send_mail
from decouple import config

class Support_View(APIView):
    
    
    def post(self, req):
        

        token = req.COOKIES.get('refresh_token')
            

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
        
        
        title = req.data.get('supportTitle')
        msg = req.data.get('supportMessage')
        cat = req.data.get('supportCategory')
        
        send_mail(
            subject=f'From autoscheduler: {title} - user: {str(user.id)}',
            message=f'Category: {cat}\n{msg}',
            recipient_list=[config('EMAIL')],
            html=''
        )
        
        return Response({'message': 'Submitted'}, status=status.HTTP_200_OK)
        
        
        
        