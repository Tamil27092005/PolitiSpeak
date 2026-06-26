"""
app.py — PolitiSpeak FastAPI entrypoint for HF Spaces
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inference import generate_audio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PolitiSpeak")

app = FastAPI(title="PolitiSpeak API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

PARTY_TO_SPEAKER = {
    "DMK"  : "stalin",
    "TVK"  : "vijay",
    "NTK"  : "seeman",
}

class AudioRequest(BaseModel):
    text  : str
    party : str

@app.get("/")
def root():
    return {"status": "PolitiSpeak API running ✅"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate-audio")
async def generate_audio_endpoint(request: AudioRequest):
    try:
        speaker   = PARTY_TO_SPEAKER.get(request.party.upper(), "seeman")
        wav_bytes = generate_audio(request.text, speaker)
        return Response(content=wav_bytes, media_type="audio/wav")
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))