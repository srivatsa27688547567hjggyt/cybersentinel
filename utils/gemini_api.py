import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def gemini_explain(log_entry, threat_level):
    """
    Generate a natural language explanation for a log entry and its threat level using Gemini 2.0 Flash.
    """
    if not GEMINI_API_KEY:
        return "Gemini API key not set. Please add it to your .env file."

    prompt = (
        f"Log Entry: {log_entry}\n"
        f"Threat Level: {threat_level}\n"
        "Explain in simple terms why this log entry might be considered this threat level."
    )

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        explanation = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No explanation returned.")
        return explanation
    except Exception as e:
        return f"Unable to generate explanation from Gemini: {str(e)}"
