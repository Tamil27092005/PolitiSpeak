# PolitiSpeak 🎙️

**Turn a tweet into a speech — literally.**

PolitiSpeak takes a political post from X (Twitter), summarizes it if needed, and converts it into Tamil audio that sounds like the actual politician being talked about — using AI voice cloning, not pre-recorded clips.

---

## The Problem

Political opinions, statements, and reactions move fast on X — but they're consumed as silent text in a feed, scrolled past in seconds. A tweet *about* a politician's stance doesn't carry their voice, tone, or presence. There's a gap between "reading what was said" and "hearing it said."

PolitiSpeak closes that gap: paste a tweet or upload the image of release, pick the politician it's about (or quoting, or replying to), and hear that text spoken back in a voice modeled on real public speech from that figure.

---

## How It Works (in plain terms)

1. **Input** — Paste a tweet's text directly, or upload a screenshot of one (text is auto-extracted from the image).
2. **Summarize (optional)** — Long threads or quote-tweets get condensed into a short, clear summary first.
3. **Text-to-Speech** — The text is converted into a neutral spoken Tamil voice.
4. **Voice Conversion** — That neutral voice is reshaped to match the vocal identity of the selected political figure, using an AI model trained on real reference speech samples.
5. **Output** — A playable audio clip, with the original tweet text always shown alongside it for full transparency.

---

## Built for How Twitter Actually Gets Used

- **Party-based voice selection** — pick the politician by party (DMK, TVK, etc.) the same way you'd tag them in a reply.
- **Screenshot-to-audio** — paste a tweet screenshot directly; no need to retype quoted text.
- **Auto-summarization for threads** — long quote-tweet chains or statements get compressed before narration, so the audio stays tight and listenable.
- **Shareable output** — generates a standalone audio file, easy to drop back into a reply, DM, or story.
- **Multi-speaker support** — built to scale across multiple political figures, not locked to one voice.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite) |
| Backend API | FastAPI (Python) |
| Base Tamil voice | Google TTS |
| Voice cloning | kNN-VC (k-Nearest Neighbors Voice Conversion) over WavLM speech representations |
| Vocoder (audio reconstruction) | HiFi-GAN |
| Text summarization | LLM-based summarization (Groq / Mistral) |
| Hosting | Hugging Face Spaces (Docker), model assets on Hugging Face Datasets |

---

## Architecture

```
Tweet (text / screenshot)
        │
        ▼
  Text Extraction + Cleaning
        │
        ▼
  Summarization (if long) ──▶ LLM API
        │
        ▼
   Tamil Text-to-Speech (gTTS)
        │
        ▼
  Speech Feature Extraction (WavLM)
        │
        ▼
  k-NN Voice Matching (against target speaker's reference voice bank)
        │
        ▼
   Vocoder Reconstruction (HiFi-GAN)
        │
        ▼
    Final Audio Output (.wav)
```

The voice-cloning core uses **kNN-VC**: source speech and a bank of real reference clips from the target speaker are both encoded into a shared feature space, then new audio is reconstructed by finding the closest-matching reference segments frame-by-frame. This means adding a new "voice" just requires clean reference clips — no retraining a model from scratch for every new speaker.

---

## What This Project Demonstrates

- **End-to-end ML system design** — a working pipeline from raw tweet text to deployed audio output, not just a notebook experiment.
- **Applied audio ML** — speech representation learning (WavLM), non-parametric voice conversion (kNN-VC), and neural vocoding (HiFi-GAN) used together in a practical product.
- **Full-stack delivery** — React frontend, FastAPI backend, containerized deployment on Hugging Face Spaces, model assets versioned separately on Hugging Face Datasets.
- **Debugging real production issues** — isolating an audio quality regression to a specific blending step in the pipeline, fixing checkpoint path/config mismatches across local and cloud environments, and resolving cross-environment deployment bugs.
- **Pragmatic engineering tradeoffs** — choosing a non-parametric voice conversion approach (kNN-VC) over a fully custom-trained TTS model to fit time and compute constraints, while keeping a clear upgrade path.

---

## Status

Active personal/portfolio project. Voice cloning quality is functional but still being refined — ongoing work includes expanding reference audio per speaker and exploring more expressive source TTS models to improve emotional tone in the output.

---

## Disclaimer

This project is built for educational and portfolio purposes to demonstrate applied AI/ML and full-stack engineering skills. It recreates the *vocal characteristics* of public figures speaking text drawn from public social media posts; it does not represent the politicians' actual statements, voices, or endorsements, and is not intended to misrepresent any individual's real speech.
