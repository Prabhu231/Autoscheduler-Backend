from django.urls import path
from .views import Forgot_Password_View

urlpatterns = [
    path('', Forgot_Password_View.as_view())
]