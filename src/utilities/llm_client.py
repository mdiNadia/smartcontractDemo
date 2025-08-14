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
import time
import requests
from config import GEMINI_API_KEY, G_MODEL_NAME

# آدرس API با مدل مشخص
url = f"https://generativelanguage.googleapis.com/v1beta/models/{G_MODEL_NAME}:generateContent"

# هدرها
headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": GEMINI_API_KEY
}

def get_summary(prompt: str, max_retries=5, base_delay=2) -> str:
    """
    ارسال درخواست به Gemini API با مکانیزم retry برای هندل کردن خطاهای موقتی (مثل 503)
    """
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()  # اگر خطا داشت، اینجا می‌پره به except

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

        except requests.exceptions.HTTPError as e:
            if response.status_code in (429, 500, 502, 503, 504):
                wait_time = base_delay * (2 ** (attempt - 1))
                print(f"[Retry {attempt}/{max_retries}] Server error {response.status_code}, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise  # اگر خطا از نوع دیگه بود، مستقیم بنداز بیرون
        except (requests.exceptions.RequestException, ValueError) as e:
            wait_time = base_delay * (2 ** (attempt - 1))
            print(f"[Retry {attempt}/{max_retries}] Error: {e}, waiting {wait_time}s...")
            time.sleep(wait_time)

    raise RuntimeError(f"Failed after {max_retries} retries.")

if __name__ == "__main__":
    prompt = """Summarize the following steps:
1. constructor
2. allowance
3. approve
4. transferFrom"""

    try:
        summary = get_summary(prompt)
        print("Summary:\n", summary)
    except Exception as e:
        print("Final error:", e)
