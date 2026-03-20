from django.urls import path
from .views import create_quiz

urlpatterns = [
    path("create/", create_quiz),
]