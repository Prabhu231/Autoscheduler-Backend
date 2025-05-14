from django.urls import path
from .views import Logout_View

urlpatterns = [
    path('', Logout_View.as_view())
]