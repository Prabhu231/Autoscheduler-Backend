from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from app.models import User
from jwt.exceptions import PyJWTError, ExpiredSignatureError, DecodeError
import jwt

class Check_View(APIView):
    
    def get(self, req):
        
        token = req.COOKIES.get('refresh_token')
            

        if not token:
            return Response({'error': 'This particular link is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,  
                algorithms=["HS256"]
            )
            User.objects.get(id=decoded_token['user_id'])

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
        
        return Response({'message': 'okay'}, status=status.HTTP_202_ACCEPTED)
        
        