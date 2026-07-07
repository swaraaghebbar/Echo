import whisper

model = whisper.load_model("base")  # or "tiny", "small"

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

