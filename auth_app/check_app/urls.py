from django.urls import path
from .views import Check_View

urlpatterns = [
    path('', Check_View.as_view())
]