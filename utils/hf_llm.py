import requests
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

MODEL = "meta-llama/Llama-3.1-8B-Instruct"
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
            "max_new_tokens": 400,
            "return_full_text": False
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    return response.json()[0]["generated_text"]
