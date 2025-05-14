from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import jwt
from django.conf import settings
from app.models import User

@method_decorator(csrf_exempt, name='dispatch')
class Logout_View(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({"error": "No token provided"}, status=400)

            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload.get('user_id'))
            user.blacklist_token = refresh_token
            user.save()

            response = Response({"message": "Logout successful"})
            response.delete_cookie('refresh_token')  
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=400)
