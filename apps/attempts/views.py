from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

from .models import Attempt, Answer
from apps.quizzes.models import Question
from .serializers import AnswerInputSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_attempt(request, attempt_id):
    try:
        attempt = Attempt.objects.get(id=attempt_id, user=request.user)
    except Attempt.DoesNotExist:
        return Response({"error": "Attempt not found"}, status=404)

    # Prevent resubmission
    if attempt.completed_at:
        return Response({"error": "Attempt already submitted"}, status=400)

    serializer = AnswerInputSerializer(data=request.data.get("answers"), many=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    answers_data = serializer.validated_data

    score = 0
    seen_questions = set()

    for ans in answers_data:
        question_id = ans["question_id"]

        # Prevent duplicate answers
        if question_id in seen_questions:
            return Response({"error": "Duplicate question in submission"}, status=400)

        seen_questions.add(question_id)

        try:
            question = Question.objects.get(id=question_id, quiz=attempt.quiz)
        except Question.DoesNotExist:
            return Response({"error": "Invalid question for this quiz"}, status=400)

        is_correct = ans["selected_option"] == question.correct_answer

        if is_correct:
            score += 1

        Answer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=ans["selected_option"],
            is_correct=is_correct
        )

    attempt.score = score
    attempt.completed_at = timezone.now()
    attempt.save()

    return Response({
        "message": "Attempt submitted successfully",
        "score": score,
        "total": len(answers_data)
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_attempt(request):
    quiz_id = request.data.get("quiz_id")

    attempt = Attempt.objects.create(
        user=request.user,
        quiz_id=quiz_id
    )

    return Response({
        "attempt_id": attempt.id,
        "message": "Attempt started"
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_history(request):
    attempts = Attempt.objects.filter(user=request.user)

    data = [
        {
            "quiz_id": a.quiz.id,
            "score": a.score,
            "total": a.answers.count(),
            "completed_at": a.completed_at
        }
        for a in attempts
    ]

    return Response(data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_stats(request):
    attempts = Attempt.objects.filter(user=request.user, completed_at__isnull=False)

    total_attempts = attempts.count()
    total_score = sum(a.score for a in attempts)

    total_questions = sum(a.answers.count() for a in attempts)

    accuracy = (total_score / total_questions * 100) if total_questions else 0

    return Response({
        "total_attempts": total_attempts,
        "average_score": total_score / total_attempts if total_attempts else 0,
        "accuracy": round(accuracy, 2)
    })