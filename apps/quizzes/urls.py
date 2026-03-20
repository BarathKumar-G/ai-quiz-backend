from django.urls import path
from .views import create_quiz, get_quiz

urlpatterns = [
    path("create/", create_quiz),
    path("<int:quiz_id>/", get_quiz),
]