from django.urls import path
from .views import Support_View

urlpatterns = [
    path('', Support_View.as_view())
]