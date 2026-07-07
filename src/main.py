import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import re
import time

from whisper_back import transcribe_audio
from llm_back import ask_llm
from tts_back import speak
from system_control import execute_system_command
from camera import capture_image
from vision import analyze_image


# EXIT PHRASES
_FILLER = {"please", "now", "hey", "ok", "okay", "computer", "jarvis", "friday", "ai"}
_EXIT_PHRASES = {
    "exit", "quit", "stop", "bye", "goodbye",
    "shut down", "power off", "stop listening"
}

def is_exit(text: str) -> bool:
    if not text:
        return False
    s = re.sub(r"[^\w\s]", "", text.lower()).strip()
    tokens = [t for t in s.split() if t not in _FILLER]
    if not tokens:
        return False
    return " ".join(tokens) in _EXIT_PHRASES


# AUDIO RECORDING
def record_audio(filename="input.wav", sr=16000):
    print("🎤 Speak now (press ENTER to stop)...")
    chunks = []

    def callback(indata, frames, time, status):
        chunks.append(indata.copy())

    with sd.InputStream(samplerate=sr, channels=1, dtype="int16", callback=callback):
        input()

    audio = np.concatenate(chunks, axis=0)
    write(filename, sr, audio)
    return filename



# Vision trigger phrases
VISION_KEYWORDS_USER = [
    "what is this",
    "what's this",
    "what am i looking at",
    "describe this",
    "look at this",
    "look at it",
    "see this",
    "identify this",
]

VISION_KEYWORDS_LLM = [
    "take a picture",
    "taking a picture",
    "i will take a picture",
    "capturing image",
    "i'll take a photo",
    "taking photo",
]


def user_requests_vision(text: str) -> bool:
    if not text:
        return False
    t = text.lower().strip()
    return any(k in t for k in VISION_KEYWORDS_USER)


def llm_requests_vision(reply: str) -> bool:
    if not reply:
        return False
    t = reply.lower().strip()
    return any(k in t for k in VISION_KEYWORDS_LLM)



# MAIN LOOP
def main():
    while True:
        try:
            # 1️⃣ LISTEN
            input_file = record_audio()
            transcript = transcribe_audio(input_file)
            print(f"User: {transcript}")

            # EXIT?
            if is_exit(transcript):
                speak("Goodbye")
                print("Exiting...")
                break

            # 2️⃣ SYSTEM COMMAND DETECTION
            sys_res = execute_system_command(transcript)
            print("DEBUG SYSTEM RESPONSE:", sys_res)

            if sys_res["executed"]:
                speak(sys_res["message"])
                continue

            if sys_res["message"] != "not_system":
                speak(sys_res["message"])
                continue

            # 3️⃣ USER DIRECTLY REQUESTS VISION
            if user_requests_vision(transcript):
                speak("Okay, taking a picture.")
                img = capture_image()
                vision_result = analyze_image(img)

                # Ask LLM to create a concise spoken response
                short_reply = ask_llm(
                    f"Summarize the following image analysis in one short, natural spoken sentence, "
                    f"without unnecessary details:\n\n{vision_result}"
                )
                print("Vision:", short_reply)
                speak(short_reply)
                continue

            # 4️⃣ ASK LLM
            reply = ask_llm(transcript)
            print(f"AI: {reply}")

            # 5️⃣ LLM REQUESTS VISION (second trigger)
            if llm_requests_vision(reply):
                speak("Taking a picture.")
                img = capture_image()
                vision_result = analyze_image(img)

                # Summarize for spoken output
                concise_reply = ask_llm(
                    f"Summarize the following image analysis in one short spoken sentence:\n\n{vision_result}"
                )
                print("Vision:", concise_reply)
                speak(concise_reply)
                continue

            # 6️⃣ NORMAL REPLY
            speak(reply)


        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break

        except Exception as e:
            print("Error:", e)
            speak("Something went wrong. Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    main()
