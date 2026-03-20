# API Documentation

## Base URL


https://your-domain/api/


---

## Authentication

This API uses JWT (JSON Web Token) authentication.

Include the following header for protected endpoints:


Authorization: Bearer <access_token>


---

## Authentication APIs

### Register User

**POST** `/api/users/register/`

Request Body:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "123456"
}

Response:

{
  "message": "User created successfully"
}
Obtain JWT Token

POST /api/token/

Request Body:

{
  "username": "testuser",
  "password": "123456"
}

Response:

{
  "refresh": "token",
  "access": "token"
}
Refresh Token

POST /api/token/refresh/

Request Body:

{
  "refresh": "your_refresh_token"
}

Response:

{
  "access": "new_access_token"
}
Quiz APIs
Create Quiz (AI-powered)

POST /api/quizzes/create/

Headers:

Authorization: Bearer <access_token>

Request Body:

{
  "topic": "Python",
  "difficulty": "easy",
  "total_questions": 5
}

Response:

{
  "message": "Quiz created successfully",
  "quiz_id": 1,
  "questions_created": 5
}

Notes:

Automatically generates questions using AI

Questions are stored in the database

Get Quiz with Questions

GET /api/quizzes/{id}/

Headers:

Authorization: Bearer <access_token>

Response:

{
  "id": 1,
  "topic": "Python",
  "difficulty": "easy",
  "total_questions": 5,
  "created_at": "2025-01-01T10:00:00Z",
  "questions": [
    {
      "id": 1,
      "text": "What is Python?",
      "options": {
        "A": "Language",
        "B": "Snake",
        "C": "Car",
        "D": "Tool"
      }
    }
  ]
}
List User Quizzes

GET /api/quizzes/

Headers:

Authorization: Bearer <access_token>

Response:

[
  {
    "id": 1,
    "topic": "Python",
    "difficulty": "easy",
    "total_questions": 5
  }
]
Attempt APIs
Start Quiz Attempt

POST /api/attempts/start/

Headers:

Authorization: Bearer <access_token>

Request Body:

{
  "quiz_id": 1
}

Response:

{
  "attempt_id": 1,
  "message": "Attempt started"
}
Submit Quiz Attempt

POST /api/attempts/{id}/submit/

Headers:

Authorization: Bearer <access_token>

Request Body:

{
  "answers": [
    {
      "question_id": 1,
      "selected_option": "A"
    },
    {
      "question_id": 2,
      "selected_option": "C"
    }
  ]
}

Response:

{
  "score": 4,
  "total": 5,
  "message": "Attempt submitted successfully"
}
Analytics APIs
User Quiz History

GET /api/users/history/

Headers:

Authorization: Bearer <access_token>

Response:

[
  {
    "quiz_id": 1,
    "score": 4,
    "total_questions": 5
  }
]
User Statistics

GET /api/users/stats/

Headers:

Authorization: Bearer <access_token>

Response:

{
  "total_attempts": 10,
  "average_score": 3.8,
  "accuracy": 76
}
Error Responses
Unauthorized
{
  "detail": "Authentication credentials were not provided."
}
Invalid Token
{
  "detail": "Given token not valid"
}
Validation Error
{
  "error": "Invalid input data"
}
Notes

All protected endpoints require JWT authentication

Users can only access their own quizzes and attempts

AI-generated content is validated before storing

System ensures fallback-safe behavior in case of AI failures