import json
import subprocess

VIDEO_FILE = "input.mp4"
OUTPUT_FILE = "teaser.mp4"
SNIPPETS_FILE = "snippets.json"
MAX_SNIPPETS = 5  # pick top 5 segments for teaser

# Load snippets
with open(SNIPPETS_FILE, "r", encoding="utf-8") as f:
    snippets = json.load(f)

# Pick first MAX_SNIPPETS segments
selected_snippets = snippets[:MAX_SNIPPETS]

# Temporary files for each clip
clip_files = []

for i, seg in enumerate(selected_snippets, 1):
    start = seg["start"]
    end = seg["end"]
    clip_file = f"clip_{i}.mp4"
    clip_files.append(clip_file)

    cmd = [
        "ffmpeg",
        "-y",  # overwrite if exists
        "-i", VIDEO_FILE,
        "-ss", start,
        "-to", end,
        "-c", "copy",
        clip_file
    ]
    subprocess.run(cmd)

# Merge clips into teaser
with open("clips.txt", "w") as f:
    for clip in clip_files:
        f.write(f"file '{clip}'\n")

subprocess.run([
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", "clips.txt",
    "-c", "copy",
    OUTPUT_FILE
])

print(f"✅ Teaser video created: {OUTPUT_FILE}")
