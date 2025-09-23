import yt_dlp

url = "https://www.youtube.com/watch?v=0FUFewGHLLg"

ydl_opts = {
    "format": "best",
    "outtmpl": "input.mp4"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("✅ Video downloaded as input.mp4")
