"""
Windows-Only System Control — Simple, Shell-Based, Fast
"""

import subprocess
import webbrowser
import urllib.parse
import pyautogui
import time
import re
from pathlib import Path

from llm_back import ask_llm   # <-- Needed for generation-typing


# ----------------------------------------------------
# Safe-ish shell executor
# ----------------------------------------------------
def run(cmd: str):
    """Run a Windows shell command."""
    try:
        subprocess.Popen(cmd, shell=True)
        return True, f"Executed: {cmd}"
    except Exception as e:
        return False, str(e)


# ----------------------------------------------------
# Command Parsing
# ----------------------------------------------------
def parse_command(text: str):
    text = text.lower().strip()

    # Remove punctuation
    if text.endswith((".", ",", "!", "?", ";", ":")):
        text = text[:-1].strip()

    # ------------------------------
    # OPEN APPS
    # ------------------------------
    if text.startswith("open "):
        app = text.replace("open ", "").strip()
        return {"type": "open", "target": app}

    # ------------------------------
    # WEB SEARCH
    # ------------------------------
    if text.startswith("search for "):
        query = text.replace("search for ", "")
        return {"type": "search", "target": query}

    if text.startswith("search "):
        query = text.replace("search ", "")
        return {"type": "search", "target": query}

    if text.startswith("google "):
        query = text.replace("google ", "")
        return {"type": "search", "target": query}

    # ------------------------------
    # CREATE FOLDER
    # ------------------------------
    if text.startswith("create folder "):
        name = text.replace("create folder ", "").strip()
        return {"type": "folder", "target": name}

    # ------------------------------
    # DIRECT TYPE COMMAND
    # ------------------------------
    if text.startswith("type "):
        msg = text.replace("type ", "").strip()
        return {"type": "typing", "target": msg}

    # ------------------------------
    # GENERATION COMMANDS (LLM → typing)
    # ------------------------------
    GENERATION_PREFIXES = [
        "generate", "write", "make", "compose", "create", "produce",
        "make me", "give me", "draft"
    ]

    # Detect if user is asking to *generate content*
    if any(text.startswith(p) for p in GENERATION_PREFIXES):
        return {"type": "generate_text", "target": text}

    # ------------------------------
    # CALCULATOR
    # ------------------------------
    if re.match(r"^[0-9+\-*/(). ]+$", text):
        return {"type": "calc", "target": text}

    return {"type": "none"}


# ----------------------------------------------------
# Command Executors
# ----------------------------------------------------

APP_COMMANDS = {
    "browser": r'start chrome',
    "chrome": r'start chrome',
    "edge": r'start msedge',
    "notepad": r'notepad',
    "code": r'code',
    "vscode": r'code',
    "explorer": r'explorer',
    "calculator": r'calc',
    "calc": r'calc',
    "terminal": r'start cmd',
    "cmd": r'start cmd',
    "spotify": r'start spotify',
}

def open_app(app: str):
    if app not in APP_COMMANDS:
        return False, f"Unknown app: {app}"
    return run(APP_COMMANDS[app])

def search_web(query: str):
    encoded = urllib.parse.quote(query)
    webbrowser.open(f"https://www.google.com/search?q={encoded}")
    return True, f"Searching for {query}"

def create_folder(name: str):
    try:
        p = Path(name)
        p.mkdir(exist_ok=True)
        return True, f"Created folder: {name}"
    except:
        return False, "Folder creation failed"

def type_text(msg: str):
    time.sleep(0.5)
    pyautogui.typewrite(msg, interval=0.03)
    return True, f"Typed text."

def calculator_input(expr: str):
    run("calc")
    time.sleep(1)
    pyautogui.typewrite(expr)
    pyautogui.press("enter")
    return True, f"Computed: {expr}"


# ----------------------------------------------------
# Main System Command Entry Point
# ----------------------------------------------------
def execute_system_command(text: str) -> dict:
    intent = parse_command(text)

    if intent["type"] == "none":
        return {"executed": False, "message": "not_system"}

    t = intent["type"]
    x = intent["target"]

    # OPEN APP
    if t == "open":
        ok, msg = open_app(x)
        return {"executed": ok, "message": msg}

    # WEB SEARCH
    if t == "search":
        ok, msg = search_web(x)
        return {"executed": ok, "message": msg}

    # CREATE FOLDER
    if t == "folder":
        ok, msg = create_folder(x)
        return {"executed": ok, "message": msg}

    # DIRECT TYPING
    if t == "typing":
        ok, msg = type_text(x)
        return {"executed": ok, "message": msg}

    # GENERATED TEXT → TYPE IT
    if t == "generate_text":
        generated = ask_llm(x)   # LLM writes content
        ok, msg = type_text(generated)
        return {"executed": ok, "message": "Generated + typed text."}

    # CALCULATOR
    if t == "calc":
        ok, msg = calculator_input(x)
        return {"executed": ok, "message": msg}

    return {"executed": False, "message": "Unknown command"}
