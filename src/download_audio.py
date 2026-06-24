import yt_dlp
import os
import sys

# Load URLs from text file
with open("data/urls.txt") as f:
    urls = [line.strip() for line in f if line.strip()]

# Make sure the output directory exists
output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}

successful = []
failed = []

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for url in urls:
        print(f"Downloading: {url}")
        try:
            ydl.download([url])
            successful.append(url)
        except Exception as e:
            print(f"❌ Skipping {url} — {e}")
            failed.append(url)

# Write failed URLs to a new file
if failed:
    with open("data/remaining_urls.txt", "w") as f:
        for url in failed:
            f.write