import whisper

# Load Whisper model (small = balance of speed & accuracy)
print("🔄 Loading Whisper model...")
model = whisper.load_model("small")

# Transcribe the video with live segment printing
print("🔄 Transcribing input.mp4...")
result = model.transcribe("input.mp4", verbose=True)

# Save transcript with timestamps
with open("transcript.txt", "w", encoding="utf-8") as f:
    for seg in result["segments"]:
        start = seg['start']
        end = seg['end']
        text = seg['text']
        f.write(f"{start:.2f} --> {end:.2f}: {text}\n")

print("✅ Transcript saved as transcript.txt")
