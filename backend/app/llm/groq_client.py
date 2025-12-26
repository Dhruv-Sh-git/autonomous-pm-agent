# app/llm/groq_client.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/v1/llm/predict"  # replace with correct endpoint

def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to Groq LLM and returns the response text.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "model": "gpt-4"  # or whichever model you are using
    }

    response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    # Adjust this based on actual Groq API response structure
    return data.get("text", "")
