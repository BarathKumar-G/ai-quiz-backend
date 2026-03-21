from django.urls import path
from .views import start_attempt, submit_attempt, user_history, user_stats

urlpatterns = [
    path("start/", start_attempt),
    path("<int:attempt_id>/submit/", submit_attempt),
    path("history/", user_history),
    path("stats/", user_stats),
]