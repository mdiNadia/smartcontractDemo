# from openai import OpenAI
# from config import OPENAI_API_KEY, MODEL_NAME

# client = OpenAI(api_key=OPENAI_API_KEY)

# def get_summary(prompt: str) -> str:
#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content.strip()

import os
import requests
from config import GEMINI_API_KEY, g_MODEL_NAME

# آدرس API با مدل مشخص
url = f"https://generativelanguage.googleapis.com/v1beta/models/{g_MODEL_NAME}:generateContent"

# هدرها
headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": GEMINI_API_KEY
}

def get_summary(prompt: str) -> str:
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # بررسی خطای HTTP
    result = response.json()

    # بررسی وجود candidates
    candidates = result.get("candidates")
    if not candidates:
        raise ValueError("API response has no candidates. Check your API key and prompt.")

    # دسترسی به content (دیکشنری)
    content_dict = candidates[0].get("content")
    if not content_dict:
        raise ValueError("Candidate has no content. Check the model and prompt.")

    # دسترسی به parts (آرایه)
    parts = content_dict.get("parts")
    if not parts:
        raise ValueError("Content has no parts.")

    # دسترسی به متن واقعی
    text_output = parts[0].get("text")
    if not text_output:
        raise ValueError("Part has no text.")

    return text_output.strip()

if __name__ == "__main__":
    prompt = """Summarize the following steps:
1. constructor
2. allowance
3. approve
4. transferFrom"""
    
    summary = get_summary(prompt)
    print("Summary:\n", summary)
