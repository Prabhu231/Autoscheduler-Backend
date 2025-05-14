from django.urls import path
from .views import Auth_View

urlpatterns = [
    path('', Auth_View.as_view())
]