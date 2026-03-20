from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Quiz(models.Model):
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    total_questions = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.text