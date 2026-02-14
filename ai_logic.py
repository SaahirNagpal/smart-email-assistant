import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("Loaded OpenRouter Key:", OPENROUTER_API_KEY)


if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is missing")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def summarize_email(email_text: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # Optional but recommended by OpenRouter
        "HTTP-Referer": "http://localhost",
        "X-Title": "Smart Email Assistant"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful customer support assistant."
            },
            {
                "role": "user",
                "content": f"""
Summarize the following customer email in 3–5 concise lines.
Focus only on the main issue and important details.

Email:
{email_text}
"""
            }
        ]
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter error: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
import json
import requests

def analyze_email(email_text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Smart Email Assistant"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an email classification engine. "
                    "Return ONLY valid JSON. No explanations. No extra text."
                )
            },
            {
                "role": "user",
                "content": f"""
Classify the following email.

INTENT (choose ONE):
- refund_request
- delivery_issue
- complaint
- general_query
- positive_feedback

SENTIMENT (choose ONE):
- angry
- neutral
- positive

Return EXACTLY this JSON format:
{{
  "intent": "<one_of_the_intents>",
  "sentiment": "<one_of_the_sentiments>"
}}

Email:
{email_text}
"""
            }
        ]
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter error: {response.text}")

    content = response.json()["choices"][0]["message"]["content"]

    # HARD SAFETY: ensure valid JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "intent": "unknown",
            "sentiment": "unknown"
        }
    
def generate_reply(email_text: str, intent: str, sentiment: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Smart Email Assistant"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional customer support agent. "
                    "Write polite, concise, and realistic email replies. "
                    "Do not make promises beyond policy. "
                    "Do not mention AI."
                )
            },
            {
                "role": "user",
                "content": f"""
Customer email:
{email_text}

Detected intent: {intent}
Detected sentiment: {sentiment}

Write a professional reply email.
Tone must match the sentiment.
Keep it concise and human-like.
"""
            }
        ]
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter error: {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()
