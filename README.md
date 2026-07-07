# 🎙️ Echo – Your Personal AI Voice Companion

Echo is a terminal-based AI assistant that lets you interact with your computer using nothing but your voice.

Instead of typing commands, you can simply speak naturally. Echo listens, understands what you mean, responds in a natural voice, and can even look at the world through your webcam whenever visual context is needed.

Whether you want to ask a question, open an application, search the web, identify an object, or generate text, Echo aims to make interacting with your computer feel conversational.

---

## ✨ Features

### 🎤 Natural Voice Conversations
- Real-time Speech-to-Text using OpenAI Whisper
- Human-like Text-to-Speech using Piper
- Context-aware conversations powered by LLaMA

---

### 👀 Vision Support

Echo doesn't just listen—it can see.

Ask things like:

> "What is this?"
>
> "Look at this."
>
> "Can you identify this object?"

Echo automatically captures an image from your webcam, analyzes it using Google Lens, and explains what it sees.

---

### 💻 Computer Control

Echo can perform everyday computer tasks, including:

- Open Chrome
- Launch VS Code
- Open Calculator
- Search Google
- Create folders
- Type generated text
- Perform calculations

All through simple voice commands.

---

### 🧠 Context-Aware Memory

Echo remembers the recent conversation so you don't need to repeat yourself every time.

You can ask follow-up questions naturally, just like talking to another person.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Speech-to-Text | Whisper |
| Language Model | LLaMA (Groq API) |
| Text-to-Speech | Piper |
| Computer Vision | Google Lens |
| Camera | OpenCV |
| Automation | PyAutoGUI |
| Voice Recording | SoundDevice |
| Language | Python |

---

## 📂 Project Structure

```
Echo/
│
├── src/
│   ├── main.py              # Main application
│   ├── whisper_back.py      # Speech recognition
│   ├── llm_back.py          # LLM integration
│   ├── tts_back.py          # Speech synthesis
│   ├── vision.py            # Image analysis
│   ├── camera.py            # Webcam capture
│   └── system_control.py    # Desktop automation
│
├── models/
│   └── Piper Voice Model
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/swaraaghebbar/Echo.git
cd Echo
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Windows

```bash
venv\Scripts\activate
```

macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```text
LLM_API=your_groq_api_key
```

### 5. Run Echo

```bash
python src/main.py
```

---

## 🎯 Example Voice Commands

```
Open Chrome

Search for the latest AI news

Create folder Projects

What is this?

Look at this object

Write a thank-you email

What is the capital of Japan?

Calculate 345 × 27
```

---
