# AI-Powered Quiz Backend

## Overview

This project is a RESTful backend system for an AI-powered quiz application built using Django and Django REST Framework. It supports user authentication, AI-driven quiz generation, quiz attempts, and performance analytics.

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)
- HuggingFace API

## Local Setup Instructions

git clone https://github.com/BarathKumar-G/ai-quiz-backend.git
cd ai-quiz-backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

Create .env:

DB_NAME=quiz_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
HF_API_KEY=your_huggingface_key

python manage.py migrate
python manage.py runserver
## Database Schema and Model Relationships

### Entities

#### User
- Extends Django's AbstractUser
- Fields: username, email, password
- Represents authenticated users of the system

#### Quiz
- Fields: topic, difficulty, total_questions, created_at
- Foreign Key: created_by → User
- Represents a quiz created by a user

#### Question
- Fields: text, options (JSONField), correct_answer
- Foreign Key: quiz → Quiz
- Stores individual questions belonging to a quiz

#### Attempt
- Fields: score, started_at, completed_at
- Foreign Keys:
  - user → User
  - quiz → Quiz
- Represents a user's attempt at a quiz

#### Answer
- Fields: selected_option, is_correct
- Foreign Keys:
  - attempt → Attempt
  - question → Question
- Stores user responses for each question in an attempt

---

### Relationships

- A User can create multiple Quizzes (1 → many)
- A Quiz contains multiple Questions (1 → many)
- A User can attempt multiple Quizzes (1 → many)
- Each Attempt belongs to one Quiz and one User
- Each Attempt contains multiple Answers (1 → many)
- Each Answer corresponds to one Question

---

### Design Considerations

- Normalized schema ensures scalability and avoids redundancy
- Separation of Attempt and Answer enables detailed analytics
- JSONField used for flexible storage of question options
- Relationships enable tracking user performance per quiz

### Authentication

POST /api/users/register/  
POST /api/token/  
POST /api/token/refresh/  

---

### Quiz

POST /api/quizzes/create/  
GET /api/quizzes/{id}/  
GET /api/quizzes/   (list user quizzes)  

---

### Attempt

POST /api/attempts/start/  
POST /api/attempts/{id}/submit/  

---

### Analytics

GET /api/users/history/  
GET /api/users/stats/  

## Design Decisions and Trade-offs

- Used JWT for stateless authentication instead of session-based authentication for scalability.
- Designed normalized relational models instead of storing quiz data as blobs.
- Used JSONField for storing options to allow flexible schema.
- Implemented service layer for AI integration to separate business logic from views.

---

## Challenges Faced and Solutions

### AI Response Parsing

HuggingFace models often return unstructured output.

**Solution:**
- Implemented JSON extraction logic
- Added validation before saving data

### Authentication Design

Needed a scalable and API-friendly authentication mechanism.

**Solution:**
- Implemented JWT authentication using SimpleJWT

### Database Design

Avoided tightly coupled or nested structures.

**Solution:**
- Designed separate models for quiz, questions, attempts, and answers

---

## AI Integration Approach

- Integrated HuggingFace inference API for question generation
- Used prompt engineering to enforce structured responses
- Implemented parsing logic to extract valid JSON
- Designed fallback-safe architecture for reliability

---

## Testing Approach

- Tested APIs using Postman
- Verified database operations using Django shell
- Tested authentication and authorization flows
- Checked cases such as unauthorized access

---

## Future Improvements

- Improve AI output reliability and formatting
- Add retry mechanisms for AI failures
