from rest_framework import serializers
from .models import Quiz,Question

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "topic", "difficulty", "total_questions", "created_at"]
        read_only_fields = ["id", "created_at"]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "options"]

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "topic",
            "difficulty",
            "total_questions",
            "questions"
        ]