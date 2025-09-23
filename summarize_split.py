import os
import json
import re
from openai import OpenAI

# ------------------------
# CONFIG
# ------------------------
LINES_PER_CHUNK = 150  # adjust as needed
MODEL = "gpt-3.5-turbo"

# ------------------------
# Load API key from environment
# ------------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")

client = OpenAI(api_key=api_key)

# ------------------------
# Read transcript
# ------------------------
with open("transcript.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# ------------------------
# Split transcript into chunks
# ------------------------
chunks = [lines[i:i+LINES_PER_CHUNK] for i in range(0, len(lines), LINES_PER_CHUNK)]

all_snippets = []

# ------------------------
# Function to fix invalid seconds
# ------------------------
def fix_timestamp(ts):
    try:
        h, m, s = map(int, ts.split(":"))
        if s >= 60:
            m += s // 60
            s = s % 60
        if m >= 60:
            h += m // 60
            m = m % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
    except:
        return ts

# ------------------------
# Process each chunk
# ------------------------
for idx, chunk_lines in enumerate(chunks, 1):
    chunk_text = "".join(chunk_lines)
    prompt = f"""
Here is a transcript chunk with timestamps:
{chunk_text}

Pick the 3-5 most engaging/important snippets with start and end times.
Return them in this JSON format:
[{{"start": "00:01:23", "end": "00:02:10"}}, ...]
"""
    print(f"Processing chunk {idx}/{len(chunks)}...")
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    output_text = resp.choices[0].message.content

    # Clean output (remove ```json etc.)
    clean_text = re.sub(r"```.*?```", "", output_text, flags=re.DOTALL).strip()

    # Try to parse JSON
    try:
        snippets = json.loads(clean_text)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", clean_text, flags=re.DOTALL)
        if match:
            snippets = json.loads(match.group(0))
        else:
            print(f"⚠️ Could not parse chunk {idx} output. Skipping.")
            snippets = []

    # Fix timestamps
    for seg in snippets:
        seg["start"] = fix_timestamp(seg["start"])
        seg["end"] = fix_timestamp(seg["end"])

    all_snippets.extend(snippets)

# ------------------------
# Save final snippets.json
# ------------------------
with open("snippets.json", "w", encoding="utf-8") as f:
    json.dump(all_snippets, f, indent=2)

print(f"✅ All snippets saved to snippets.json ({len(all_snippets)} segments)")
