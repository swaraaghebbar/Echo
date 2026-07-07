import sounddevice as sd
import numpy as np
from piper import PiperVoice
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)
model = os.path.join(REPO_ROOT, "models", "en_GB-jenny_dioco-medium.onnx")

voice = PiperVoice.load(model)
SAMPLE_RATE = voice.config.sample_rate

def speak(text):
    """Generate speech and play it directly."""

    #collect PCM16 chunks
    audio_chunks = [chunk.audio_int16_bytes for chunk in voice.synthesize(text)]

    #join into one byte stream
    audio_bytes = b"".join(audio_chunks)

    #convert bytes -> numpy array
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

    #play back
    sd.play(audio_np, samplerate=SAMPLE_RATE)
    sd.wait()

    return f"Played {len(audio_np)} samples in real-time"