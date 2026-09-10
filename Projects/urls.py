from django.urls import path
from .views import *
urlpatterns = [
    path('create/',CreateProjectAPIView.as_view())
]