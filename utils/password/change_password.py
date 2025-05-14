from app.models import User
import bcrypt
from rest_framework.response import Response
from rest_framework import status

def change_password(user: User, password):
    
    if password:
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password = hashed_password
            user.save()
            return Response({'message': 'Password updated successfully'})
        except Exception as e:
            return Response({'error': f'Error while updating the password: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response({'message': 'Link is valid'}, status=status.HTTP_200_OK)