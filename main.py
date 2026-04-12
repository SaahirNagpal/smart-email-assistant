from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from ai_logic import process_email_ai
import os

app = FastAPI()

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
@app.get("/")
def home():
    return FileResponse("index.html")


class EmailRequest(BaseModel):
    email_text: str


@app.post("/process-email")
def process_email(request: EmailRequest):
    try:
        result = process_email_ai(request.email_text)
        return result
    except Exception as e:
        print("BACKEND ERROR:", str(e))
        return {
            "summary": "Error occurred",
            "intent": "error",
            "sentiment": "error",
            "suggested_reply": str(e)
        }