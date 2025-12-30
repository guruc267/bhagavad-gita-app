import requests
import os
import time

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def get_telugu_bhavam(sloka_text):
    prompt = f"""
క్రింది భగవద్గీత శ్లోకాన్ని
తెలుగులో సులభమైన భాషలో
భావంతో వివరించండి.

శ్లోకం:
{sloka_text}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.4,
            "max_new_tokens": 300,
            "return_full_text": False
        }
    }

    for _ in range(3):  # retry logic
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return data[0]["generated_text"]
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
            else:
                return str(data)

        elif response.status_code == 503:
            time.sleep(5)  # model loading, wait and retry
        else:
            return f"⚠️ Hugging Face Error: {response.status_code}"

    return "⚠️ Hugging Face model busy. Please try again."
