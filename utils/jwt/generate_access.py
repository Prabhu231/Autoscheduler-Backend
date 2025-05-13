import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings

def refresh_access_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])

        if payload.get('type') != 'refresh':
            return {'error': 'Invalid token type'}
        
        now = datetime.now(timezone.utc)

        expiration_time = now + timedelta(minutes=15)

        user_id = payload.get('user_id')
        new_access_payload = {
            'user_id': user_id,
            "iat": int(now.timestamp()),
            "exp": int(expiration_time.timestamp()),  
            'type': 'access'
        }
        new_access_token = jwt.encode(new_access_payload, settings.SECRET_KEY, algorithm='HS256')
        return {'access_token': new_access_token}

    except jwt.ExpiredSignatureError:
        return {'error': 'Refresh token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid refresh token'}
