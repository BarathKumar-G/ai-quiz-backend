from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz
from .serializers import QuizSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_quiz(request):
    serializer = QuizSerializer(data=request.data)

    if serializer.is_valid():
        quiz = serializer.save(created_by=request.user)

        return Response(
            {
                "message": "Quiz created successfully",
                "quiz_id": quiz.id
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)