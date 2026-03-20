import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def generate_questions(topic, difficulty, num_questions):
    prompt = f"""
    Generate {num_questions} multiple choice questions on topic '{topic}' with difficulty '{difficulty}'.
    Each question should have:
    - question text
    - 4 options (A, B, C, D)
    - correct answer

    Return in JSON format like:
    [
      {{
        "text": "question",
        "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
        "correct_answer": "A"
      }}
    ]
    """

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    result = response.json()

    try:
        output_text = result[0]["generated_text"]

        import json
        questions = json.loads(output_text)

        return questions

    except Exception:
        return []