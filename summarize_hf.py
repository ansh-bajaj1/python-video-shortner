import json
from transformers import pipeline

# ------------------------
# CONFIG
# ------------------------
TRANSCRIPT_FILE = "transcript.txt"
OUTPUT_FILE = "snippets.json"
CHARS_PER_CHUNK = 1000  # small enough to handle CPU summarization
TOTAL_VIDEO_SECONDS = 60 * 120  # e.g., 2 hours video length

# ------------------------
# Load summarization model locally
# ------------------------
print("🔄 Loading local summarization model...")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# ------------------------
# Read transcript
# ------------------------
with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
    transcript = f.read()

total_chars = len(transcript)
chunks = [transcript[i:i+CHARS_PER_CHUNK] for i in range(0, total_chars, CHARS_PER_CHUNK)]

# ------------------------
# Approximate timestamps function
# ------------------------
def approx_timestamp(start_idx, end_idx):
    start_sec = int((start_idx / total_chars) * TOTAL_VIDEO_SECONDS)
    end_sec = int((end_idx / total_chars) * TOTAL_VIDEO_SECONDS)
    def fmt(sec):
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
    return fmt(start_sec), fmt(end_sec)

# ------------------------
# Process chunks
# ------------------------
snippets = []

for idx, chunk in enumerate(chunks, 1):
    print(f"Processing chunk {idx}/{len(chunks)}...")
    summary = summarizer(chunk, max_length=60, min_length=20, do_sample=False)[0]['summary_text']
    
    start_idx = idx*CHARS_PER_CHUNK - CHARS_PER_CHUNK
    end_idx = min(idx*CHARS_PER_CHUNK, total_chars)
    start_ts, end_ts = approx_timestamp(start_idx, end_idx)
    
    snippets.append({
        "start": start_ts,
        "end": end_ts,
        "text": summary
    })

# ------------------------
# Save snippets.json
# ------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(snippets, f, indent=2)

print(f"✅ Local summarization done! Snippets saved to {OUTPUT_FILE} ({len(snippets)} segments)")
