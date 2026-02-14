from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from ai_logic import summarize_email, analyze_email, generate_reply

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class EmailRequest(BaseModel):
    email_text: str

@app.post("/process-email")
def process_email(request: EmailRequest):
    summary = summarize_email(request.email_text)
    analysis = analyze_email(request.email_text)
    reply = generate_reply(
        request.email_text,
        analysis["intent"],
        analysis["sentiment"]
    )

    return {
        "summary": summary,
        "intent": analysis["intent"],
        "sentiment": analysis["sentiment"],
        "suggested_reply": reply
    }