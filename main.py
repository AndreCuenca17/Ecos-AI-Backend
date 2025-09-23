# apps/server/main.py (añade debajo de tus imports/route existentes)
import os, httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/speech/token")
async def get_speech_token():
    if not AZURE_SPEECH_KEY or not AZURE_SPEECH_REGION:
        return {"error": "missing_azure_env"}
    url = f"https://{AZURE_SPEECH_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {"Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY, "Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, headers=headers)
        r.raise_for_status()
        token = r.text
    return {"region": AZURE_SPEECH_REGION, "token": token}