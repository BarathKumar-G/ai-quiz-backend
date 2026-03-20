import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

import re

def extract_json(text):
    try:
        # Find JSON array inside messy text
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            return None

        json_str = match.group(0)

        import json
        return json.loads(json_str)

    except Exception as e:
        print("JSON extraction failed:", e)
        return None

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

        questions = extract_json(output_text)

        if not questions:
            raise ValueError("No valid JSON extracted")

        return questions

    except Exception:
        return []