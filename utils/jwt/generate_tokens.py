import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


def generate_jwt(user_id):
    try:
        if not user_id:
            raise ValueError("User ID is required to generate JWT.")

        if not hasattr(settings, 'SECRET_KEY') or not settings.SECRET_KEY:
            raise ValueError("SECRET_KEY is not defined in settings.")
        
        
        now = datetime.now(timezone.utc)

        expiration_time = now + timedelta(minutes=15)
        access_payload = {
                "user_id": user_id,
                "iat": int(now.timestamp()),
                "exp": int(expiration_time.timestamp()),  
                "type": "access"
        }
        
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
        
        expiration_time = now + timedelta(days=7)

        refresh_payload = {
            'user_id': user_id,
            "iat": int(now.timestamp()),
            "exp": int(expiration_time.timestamp()), 
            'type': 'refresh'
        }
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    except ValueError as ve:
        return {'error': str(ve)}
    except jwt.PyJWTError as e:
        return {'error': f'JWT generation failed: {str(e)}'}
    except Exception as ex:
        return {'error': f'Unexpected error: {str(ex)}'}
