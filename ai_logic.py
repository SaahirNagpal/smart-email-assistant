import os
import requests
import json
from dotenv import load_dotenv

# SIMPLE + RELIABLE
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is missing")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def process_email_ai(email_text: str) -> dict:
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            # THIS MODEL ACTUALLY WORKS ON FREE TIER
            "model": "meta-llama/llama-3-8b-instruct",

            "max_tokens": 200,
            "temperature": 0.7,

            "messages": [
                {
                    "role": "system",
                    "content": "You are an email assistant. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": f"""
Analyze this email and return JSON:

{{
  "summary": "...",
  "intent": "...",
  "sentiment": "...",
  "suggested_reply": "..."
}}

Email:
{email_text[:1000]}
"""
                }
            ]
        }

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        if response.status_code != 200:
            return {
                "summary": "API error",
                "intent": "error",
                "sentiment": "error",
                "suggested_reply": response.text
            }

        data = response.json()

        choices = data.get("choices")
        if not choices:
            return {
                "summary": "No response from model",
                "intent": "error",
                "sentiment": "error",
                "suggested_reply": str(data)
            }

        content = choices[0].get("message", {}).get("content", "")

        if not content:
            return {
                "summary": "Empty response",
                "intent": "error",
                "sentiment": "error",
                "suggested_reply": str(data)
            }

        import re

        try:
            # extract JSON block from response
            json_match = re.search(r"\{.*\}", content, re.DOTALL)

            if not json_match:
                raise ValueError("No JSON found")

            json_str = json_match.group()

            return json.loads(json_str)

        except Exception:
            return {
                "summary": "Parsing failed",
                "intent": "unknown",
                "sentiment": "unknown",
                "suggested_reply": content
            }

    except Exception as e:
        print("FINAL ERROR:", str(e))
        return {
            "summary": "Backend crash",
            "intent": "error",
            "sentiment": "error",
            "suggested_reply": str(e)
        }