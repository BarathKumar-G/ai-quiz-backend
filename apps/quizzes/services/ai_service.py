import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

import re
import json
def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return []



def generate_questions(topic, difficulty, num_questions):
    
    prompt = f"""
    You are an API that returns ONLY valid JSON.

    Generate {num_questions} multiple choice questions on topic "{topic}" with difficulty "{difficulty}".

    STRICT RULES:
    - Output MUST be valid JSON
    - Do NOT include explanation
    - Do NOT include text before/after JSON

    FORMAT:
    [
    {{
        "text": "question",
        "options": {{
        "A": "option",
        "B": "option",
        "C": "option",
        "D": "option"
        }},
        "correct_answer": "A"
    }}
    ]
    """
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt}
        )

        result = response.json()
        output_text = result[0]["generated_text"]

        questions = extract_json(output_text)

        return questions if questions else []

    except Exception as e:
        print("AI error:", e)
        return []