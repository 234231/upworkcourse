import os
from faster_whisper import WhisperModel

# Load the model once (Base is fast, Small is accurate)
# Set device="cpu" if you don't have an NVIDIA GPU
model = WhisperModel("small", device="cuda", compute_type="float16")

def process_audio(audio_path, output_text_path):
    print(f"Starting transcription for: {audio_path}")
    
    # beam_size=5 is the sweet spot for speed/accuracy
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    with open(output_text_path, "w", encoding="utf-8") as f:
        for segment in segments:
            # Writes time-stamped text
            line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
            f.write(line)
            
    print(f"Done! Saved to {output_text_path}")

# To test this alone, put an mp3 in the folder and run:
# process_audio("test_lecture.mp3", "transcript.txt")