import requests

def generate_questions(topic, difficulty, num_questions):
    
    questions = []

    for i in range(num_questions):
        questions.append({
            "text": f"{topic} question {i+1} ({difficulty})",
            "options": {
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            },
            "correct_answer": "A"
        })

    return questions