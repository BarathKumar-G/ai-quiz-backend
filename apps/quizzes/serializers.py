from rest_framework import serializers
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "topic", "difficulty", "total_questions", "created_at"]
        read_only_fields = ["id", "created_at"]