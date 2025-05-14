from django.urls import path
from .views import Reset_Password_View

urlpatterns = [
    path('', Reset_Password_View.as_view())
]