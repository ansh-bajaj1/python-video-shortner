import subprocess

# Replace with snippets from summarize.py output
snippets = [
    {"start": "00:01:23", "end": "00:02:10"},
    {"start": "00:04:05", "end": "00:04:50"}
]

# Cut clips
for i, s in enumerate(snippets):
    subprocess.run([
        "ffmpeg", "-i", "input.mp4", "-ss", s["start"], "-to", s["end"],
        "-c", "copy", f"clip{i}.mp4"
    ])

# Merge clips
with open("clips.txt", "w") as f:
    for i in range(len(snippets)):
        f.write(f"file 'clip{i}.mp4'\n")

subprocess.run([
    "ffmpeg", "-f", "concat", "-safe", "0", "-i", "clips.txt", "-c", "copy", "teaser.mp4"
])

print("✅ Final teaser video saved as teaser.mp4")
