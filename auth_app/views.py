from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import User
import bcrypt
from utils.jwt.generate_tokens import generate_jwt
from django.db import IntegrityError
from utils.mail.welcome_mail import send_welcome_mail
from datetime import datetime, timedelta
import jwt
from django.conf import settings

class Auth_View(APIView):
    def post(self, req):
        try:
     
            response_headers = {
                'Access-Control-Allow-Origin': settings.CORS_ALLOWED_ORIGINS[0] if hasattr(settings, 'CORS_ALLOWED_ORIGINS') and settings.CORS_ALLOWED_ORIGINS else '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            }
            
         
            auto_login = req.data.get('auto_login')
            
            if auto_login:
                print('Auto login attempted')
                print('All cookies:', req.COOKIES)
                refresh_token = req.COOKIES.get('refresh_token')
                print('refresh_token found:', refresh_token is not None)
                
                if not refresh_token:
                    response = Response({
                        'flag': 0,
                        'error': 'No refresh token found'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
                    for key, value in response_headers.items():
                        response[key] = value
                    
                    return response
                    
                try: 
                    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
                    user_id = payload.get('user_id')
                    
                    if not user_id:
                        response = Response({
                            'flag': 0,
                            'error': 'Invalid token payload'
                        }, status=status.HTTP_401_UNAUTHORIZED)
                        
                      
                        for key, value in response_headers.items():
                            response[key] = value
                            
                        return response
                    
                  
                    try:
                        user = User.objects.get(id=user_id)
                        blacklisted_token = str(user.blacklist_token)
                        if refresh_token == blacklisted_token:
                            return Response({
                                'flag': 0,
                                'error': 'Token is blacklisted'
                            })
                    except User.DoesNotExist:
                        response = Response({
                            'flag': 0,
                            'error': 'User not found'
                        }, status=status.HTTP_401_UNAUTHORIZED)
                        
                     
                        for key, value in response_headers.items():
                            response[key] = value
                            
                        return response
                    
                    
                    
                    tokens = generate_jwt(user_id)
                    
                    response = Response({
                        'flag': 1, 
                        'access_token': tokens["access_token"]
                    }, status=status.HTTP_200_OK)
                    
               
                    response.set_cookie(
                        key='refresh_token',
                        value=tokens['refresh_token'], 
                        expires=datetime.now() + timedelta(days=7),
                        httponly=True,
                        secure=settings.DEBUG is False,
                        samesite='None' if not settings.DEBUG else 'Lax', 
                        path='/', 
                    )
                    
                    for key, value in response_headers.items():
                        response[key] = value
                    
                    return response
                    
                except jwt.ExpiredSignatureError:
                    response = Response({
                        'flag': 0,
                        'error': 'Token expired'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
                   
                    for key, value in response_headers.items():
                        response[key] = value
                        
                    return response
                    
                except jwt.InvalidTokenError:
                    response = Response({
                        'flag': 0,
                        'error': 'Invalid token'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
                 
                    for key, value in response_headers.items():
                        response[key] = value
                        
                    return response
                    
                except Exception as e:
                    print(f"Auto login error: {str(e)}")
                    response = Response({
                        'flag': 0,
                        'error': 'Authentication failed'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
                 
                    for key, value in response_headers.items():
                        response[key] = value
                        
                    return response
            
         
            email = req.data.get('email')
            password = req.data.get('password')
            login_flag = req.data.get('login')
            
            if not email or not password:
                response = Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            
                for key, value in response_headers.items():
                    response[key] = value
                    
                return response

            if str(login_flag) == '1':
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    response = Response({'error': 'Email does not exist'}, status=status.HTTP_404_NOT_FOUND)
                    
                 
                    for key, value in response_headers.items():
                        response[key] = value
                        
                    return response

                if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    response = Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
                    
                
                    for key, value in response_headers.items():
                        response[key] = value
                        
                    return response

                tokens = generate_jwt(user.id)
                if tokens.get('error'):
                    response = Response({'error': 'Server error, please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
                 
                    for key, value in response_headers.items():
                        response[key] = value
                        
                    return response
                
                response = Response({
                    'access_token': tokens["access_token"],
                    'flag': 1
                }, status=status.HTTP_200_OK)
                
              
                response.set_cookie(
                    key='refresh_token',
                    value=tokens['refresh_token'], 
                    expires=datetime.now() + timedelta(days=7),
                    httponly=True,
                    secure=settings.DEBUG is False,
                    samesite='None' if not settings.DEBUG else 'Lax',  
                    path='/',  
                )
                
           
                for key, value in response_headers.items():
                    response[key] = value
                
                return response
            else:
                try:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    user = User.objects.create(email=email, password=hashed_password)
                except IntegrityError:
                    response = Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                 
                    for key, value in response_headers.items():
                        response[key] = value
                        
                    return response
                
                send_welcome_mail(recipient_list=[email])
                response = Response({'data': {'message': 'Account created successfully'}}, status=status.HTTP_201_CREATED)
                
             
                for key, value in response_headers.items():
                    response[key] = value
                    
                return response
                
        except Exception as e:
            print(f"Unexpected error")
            import traceback
            print(traceback.format_exc())

            response = Response({'error': 'Unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
   
            for key, value in response_headers.items():
                response[key] = value
                
            return response
            

    def options(self, request, *args, **kwargs):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.CORS_ALLOWED_ORIGINS[0] if hasattr(settings, 'CORS_ALLOWED_ORIGINS') and settings.CORS_ALLOWED_ORIGINS else '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Max-Age'] = '86400'  # 24 hours
        return response