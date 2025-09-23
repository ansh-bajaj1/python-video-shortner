
# Agentic AI Internship – Teaser Video Automation

This repository contains the implementation for creating a **2–3 minute teaser video** from a full-length YouTube video using **Python, Whisper, Hugging Face Transformers, and FFmpeg**.  

The workflow is fully automated, including **transcription, summarization, and video snippet merging**.

---

## **Repository Structure**

├── transcribe.py # Transcribes input video using Whisper

├── summarize_local.py # Summarizes transcript into important snippets (local model)

├── make_teaser.py # Creates teaser video using FFmpeg from selected snippets

├── transcript.txt # Sample transcript (optional)

├── snippets.json # Sample snippets generated from summarization

├── teaser.mp4 # Example output teaser (optional, not in repo)

├── README.md # This file

└── requirements.txt # Python dependencies

---

## **Workflow Overview**

1. **Video Transcription**  
   - Uses OpenAI Whisper to generate a timestamped transcript (`transcript.txt`) from `input.mp4`.  

2. **Transcript Summarization**  
   - Splits transcript into chunks to handle large input.  
   - Summarizes chunks locally using Hugging Face Transformers (BART) to pick **important snippets**.  
   - Output saved as `snippets.json`.

3. **Teaser Video Creation**  
   - Selects top 3–5 snippets from `snippets.json`.  
   - Cuts corresponding video segments from `input.mp4` using FFmpeg.  
   - Merges segments into a **2–3 minute teaser** (`teaser.mp4`).

---

## **Setup Instructions**

1. **Clone repository**  
```bash
git clone <your-repo-link>
cd <repo-folder>

Install dependencies

pip install -r requirements.txt


Prepare input video

Place your video file in the repo folder as input.mp4.

Run scripts sequentially

Step 1: Transcribe video

python transcribe.py


Step 2: Summarize transcript

python summarize_local.py


Step 3: Create teaser video

python make_teaser.py

Environment Variables

If using APIs, set the API key as an environment variable:

setx OPENAI_API_KEY "YOUR_KEY_HERE"   # Windows
export OPENAI_API_KEY="YOUR_KEY_HERE" # Linux/macOS

Challenges & Notes

Transcription is slow on CPU; patience required for long videos.

API-based summarization may hit rate limits; local models (PyTorch + Transformers) avoid this.

Large transcripts are split into chunks for processing.

Timestamps from transcript are approximated to cut accurate video segments.

When using API-based summarization initially, we faced rate-limit errors due to long transcripts. Switching to a local model with PyTorch solved this.

Outcome

snippets.json contains the most important video segments with timestamps.

teaser.mp4 is a concise 2–3 minute video teaser ready for submission.

Dependencies

Python 3.11+

whisper

torch

transformers

requests

FFmpeg installed and added to PATH

requirements.txt

whisper
torch
transformers
requests


---



whisper
torch
transformers
requests
