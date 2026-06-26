"""
inference.py — PolitiSpeak local kNN-VC pipeline
Matches Kaggle Cell 3 EXACTLY (pure kNN, no VITS blending).
Drop this into your backend\ folder
"""

import os
import sys
import glob
import logging
import tempfile
from pathlib import Path

import torch
import torchaudio
from gtts import gTTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PolitiSpeak")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent
KNNVC_DIR    = BASE_DIR / "knnvc"
REF_WAVS_DIR = KNNVC_DIR / "ref_wavs"
WAVLM_PATH   = KNNVC_DIR / "WavLM-Large.pt"
HIFIGAN_PATH = KNNVC_DIR / "prematch_g_02500000.pt"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TOPK   = 4   # matches Cell 3 exactly

# ─────────────────────────────────────────────
# GLOBALS
# ─────────────────────────────────────────────
_knn_vc = None
_speaker_matching_sets = {}   # speaker -> matching set tensor (pure kNN, untouched)


def _load_models():
    global _knn_vc

    if _knn_vc is not None:
        return

    logger.info(f"Loading kNN-VC on {DEVICE}…")

    os.environ.setdefault("TORCH_HOME", str(KNNVC_DIR.parent))
    hub_cache = Path(os.environ["TORCH_HOME"]) / "hub" / "checkpoints"
    hub_cache.mkdir(parents=True, exist_ok=True)

    for fname in ["WavLM-Large.pt", "prematch_g_02500000.pt"]:
        src = KNNVC_DIR / fname
        dst = hub_cache / fname
        if src.exists() and not dst.exists():
            import shutil
            shutil.copy2(src, dst)
            logger.info(f"Copied {fname} → hub cache")

    _knn_vc = torch.hub.load(
        "bshall/knn-vc",
        "knn_vc",
        prematched=True,
        trust_repo=True,
        pretrained=True,
        device=DEVICE,
    )
    logger.info("kNN-VC loaded ✅")

    _build_all_matching_sets()
    logger.info("Matching sets ready ✅")


def _build_all_matching_sets():
    """
    EXACT match to Kaggle Cell 2:
    matching_set = knn_vc.get_matching_set(resampled_paths)
    No projection, no blending, no normalize — raw matching set only.
    """
    global _speaker_matching_sets

    for speaker in ["stalin", "vijay"]:
        ref_dir  = REF_WAVS_DIR / speaker
        wav_list = sorted(glob.glob(str(ref_dir / "*.wav")))[:50]   # cap at 50, same as Cell 2
        if not wav_list:
            logger.warning(f"No ref wavs found for {speaker} at {ref_dir}")
            continue

        with torch.inference_mode():
            matching_set = _knn_vc.get_matching_set(wav_list)

        _speaker_matching_sets[speaker] = matching_set
        logger.info(f"{speaker}: matching_set shape → {matching_set.shape}")


# ─────────────────────────────────────────────
# MAIN INFERENCE — mirrors Cell 3's tamil_tts_voice_clone()
# ─────────────────────────────────────────────
def generate_audio(text: str, speaker: str) -> bytes:
    _load_models()
    speaker = speaker.lower()

    if speaker == "seeman" or speaker not in _speaker_matching_sets:
        logger.info(f"Speaker '{speaker}' → gTTS fallback (not in v1 kNN deployment)")
        return _gtts_fallback(text)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Step 1: gTTS → mp3
        gtts_path = tmpdir / f"gtts_raw_{speaker}.mp3"
        gTTS(text=text, lang="ta", slow=False).save(str(gtts_path))

        # Step 2: mp3 → 16kHz mono wav
        query_path = tmpdir / f"gtts_16k_{speaker}.wav"
        waveform, sr = torchaudio.load(str(gtts_path))
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
        if sr != 16000:
            waveform = torchaudio.functional.resample(waveform, sr, 16000)
        torchaudio.save(str(query_path), waveform, 16000)

        # Step 3: WavLM encode source
        with torch.inference_mode():
            query_seq = _knn_vc.get_matching_set([str(query_path)])

            # Step 4: kNN match — pure, untouched matching set (Cell 3 parity)
            out_wav = _knn_vc.match(
                query_seq,
                _speaker_matching_sets[speaker],
                topk=TOPK,
            )

        # Step 5: Save output
        out_path = tmpdir / "output.wav"
        out_wav_cpu = out_wav.cpu()
        if out_wav_cpu.dim() == 1:
            out_wav_cpu = out_wav_cpu.unsqueeze(0)   # [T] -> [1, T]
        torchaudio.save(str(out_path), out_wav_cpu, 16000)
        return out_path.read_bytes()


def _gtts_fallback(text: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        mp3 = tmpdir / "fallback.mp3"
        wav = tmpdir / "fallback.wav"
        gTTS(text=text, lang="ta").save(str(mp3))
        waveform, sr = torchaudio.load(str(mp3))
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
        if sr != 16000:
            waveform = torchaudio.functional.resample(waveform, sr, 16000)
        torchaudio.save(str(wav), waveform, 16000)
        return wav.read_bytes()

if __name__ == "__main__":
    test_text = "தமிழ்நாட்டில் மக்களுக்கு நீதி கிடைக்கும்."
    test_speaker = sys.argv[1] if len(sys.argv) > 1 else "stalin"

    print(f"Generating audio for speaker: {test_speaker}")
    wav_bytes = generate_audio(test_text, test_speaker)

    out_file = f"test_output_{test_speaker}.wav"
    Path(out_file).write_bytes(wav_bytes)
    print(f"✅ Saved → {out_file}  ({len(wav_bytes)/1024:.1f} KB)")