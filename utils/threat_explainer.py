import os
import requests
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

# Hugging Face Transformers pipeline for zero-shot classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

THREAT_LABELS = ["Low", "Medium", "High"]

# Hugging Face API key (optional, for hosted inference)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")


def explain_threat(log_entry, threat_level):
    """
    Generate a natural language explanation for a log entry and its threat level using Hugging Face Transformers.
    """
    try:
        # Use zero-shot classification to justify the threat level
        result = classifier(log_entry, THREAT_LABELS)
        top_label = result['labels'][0]
        score = result['scores'][0]
        explanation = (
            f"The log entry was classified as '{top_label}' threat with confidence {score:.2f}. "
            f"Reasoning: The model associates this log with patterns typical of {top_label} risk."
        )
        return explanation
    except Exception as e:
        return f"Unable to generate explanation: {str(e)}"