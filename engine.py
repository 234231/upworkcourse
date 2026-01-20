import yt_dlp
from faster_whisper import WhisperModel
from dotenv import load_dotenv
import os

# Initialize the High-Speed Engine
# If you have an NVIDIA GPU, use device="cuda". Otherwise use "cpu".
model = WhisperModel("small", device="cpu", compute_type="int8") 

def download_and_transcribe(video_url, title):
    audio_file = f"{title}.mp3"
    
    # 1. High-Speed Audio Extraction (No Video)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{title}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    print(f"[*] Extracting audio from: {title}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # 2. Faster-Whisper Transcription
    print(f"[*] Transcribing {title} (this may take 2-5 mins)...")
    segments, info = model.transcribe(f"downloads/{audio_file}", beam_size=5)
    
    transcript_path = f"transcripts/{title}.txt"
    with open(transcript_path, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(f"[{segment.start:.2f}s] {segment.text}\n")
    
    print(f"[+] Success! Transcript saved to {transcript_path}")