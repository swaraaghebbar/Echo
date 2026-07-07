import os
import logging
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("LLM_API")

if not API_KEY:
    raise ValueError("Missing LLM_API key in .env file")

# Initialize Groq client
client = Groq(api_key=API_KEY)

# Store chat history with metadata
class ConversationHistory:
    def __init__(self, max_turns=10):
        self.max_turns = max_turns
        self.system_prompt = (
            "You are an AI assistant with control over a real computer. "
            "When the user asks things like 'what is this?', 'look at this', "
            "'can you see this?', or anything requiring visual input, you MUST respond "
            "with a camera trigger phrase:\n\n"
            "'Okay, taking a picture now.'\n\n"
            "Do NOT say you cannot take pictures. "
            "Do NOT apologize. "
            "Do NOT refuse. "
            "Simply use the trigger phrase whenever an image is needed. "
            "Otherwise respond normally. "
            "Keep responses short, direct, and friendly."
        )
        self.history = []

    def add_turn(self, user_msg: str, ai_msg: str):
        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": ai_msg})
        
        # Keep only last N messages
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]

    def build_messages(self, new_user_msg: str):
        """Groq API expects a list of {role, content} messages."""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": new_user_msg})
        return messages

    def clear(self):
        self.history = []


# Global conversation history
conv_history = ConversationHistory(max_turns=8)


def ask_llm(user_input: str, max_words=50) -> str:
    """
    Send message to Groq LLaMA model, maintain history.
    """
    if not user_input or not user_input.strip():
        return "I didn't catch that. Could you repeat?"

    try:
        # Prepare conversation for API
        messages = conv_history.build_messages(user_input)

        # Call Groq LLaMA model
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=256,
            top_p=0.9,
        )

        # ✅ FIXED LINE — access via attributes, not dict
        reply = response.choices[0].message.content.strip()

        # Word cap
        words = reply.split()
        if len(words) > max_words:
            reply = " ".join(words[:max_words]) + "..."

        # Save conversation
        conv_history.add_turn(user_input, reply)

        return reply

    except Exception as e:
        logging.error(f"Groq LLM error: {e}")
        return "Something went wrong while thinking. Try again."


def reset_conversation():
    conv_history.clear()
    return "Conversation reset."


def get_history_summary():
    return f"Conversation has {len(conv_history.history)} messages."

def llm_requests_vision(text: str) -> bool:
    triggers = [
        "look at",
        "what is this",
        "see this",
        "take a picture",
        "use the camera",
        "capture image",
        "what do you see",
        "analyze this",
        "identify this"
    ]
    t = text.lower()
    return any(x in t for x in triggers)
