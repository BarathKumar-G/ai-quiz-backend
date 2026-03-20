from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz,Question
from .serializers import QuizSerializer
from .services.ai_service import generate_questions

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_quiz(request):
    serializer = QuizSerializer(data=request.data)

    if serializer.is_valid():
        quiz = serializer.save(created_by=request.user)

        #  Generate questions
        questions = generate_questions(
            topic=quiz.topic,
            difficulty=quiz.difficulty,
            num_questions=quiz.total_questions
        )

        # Save questions
        for q in questions:
            Question.objects.create(
                quiz=quiz,
                text=q["text"],
                options=q["options"],
                correct_answer=q["correct_answer"]
            )

        return Response(
            {
                "message": "Quiz created with questions",
                "quiz_id": quiz.id
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)