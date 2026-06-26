import sys
import os
import importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import re

try:
    edge_tts = importlib.import_module("edge_tts")
except ImportError:
    edge_tts = None

app = FastAPI()

# Allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Party → Edge-TTS voice mapping (closest available voices)
PARTY_VOICES = {
    "tvk":   "ta-IN-ValluvarNeural",   # Tamil male
    "ntk":   "ta-IN-ValluvarNeural",   # Tamil male
    "dmk":   "ta-IN-ValluvarNeural",   # Tamil male
    "admk":  "ta-IN-ValluvarNeural",   # Tamil male
    "vck":   "ta-IN-ValluvarNeural",   # Tamil male
    "mnm":   "ta-IN-ValluvarNeural",   # Tamil male
}

LANG_VOICES = {
    "tamil":   "ta-IN-ValluvarNeural",
    "hindi":   "hi-IN-MadhurNeural",
    "english": "en-IN-PrabhatNeural",
}

class AudioRequest(BaseModel):
    text: str
    party: str
    language: str

def clean_text(text: str) -> str:
    text = re.sub(r'@[\w\u0B80-\u0BFF]+', '', text)
    text = re.sub(r'#[\w\u0B80-\u0BFF]+', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

@app.post("/generate-audio")
async def generate_audio(req: AudioRequest):
    text = clean_text(req.text)

    # Pick voice — party first, fallback to language
    voice = PARTY_VOICES.get(req.party) or LANG_VOICES.get(req.language, "ta-IN-ValluvarNeural")

    output_path = f"output_{req.party}.mp3"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

    return FileResponse(
        output_path,
        media_type="audio/mpeg",
        filename="speech.mp3"
    )

@app.get("/")
def root():
    return {"status": "PolitiSpeak backend running"}