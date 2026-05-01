from flask import Flask, render_template, request, jsonify
import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

app = Flask(__name__)
_client = None
HISTORY_PATH = Path(__file__).parent / "chat_history.json"
DEMO_MODE = not os.getenv("OPENAI_API_KEY")


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        _client = OpenAI(api_key=api_key)
    return _client


def fake_reply(message: str) -> str:
    """Return a plausible-looking demo reply when no API key is configured."""
    msg = message.lower()
    if any(w in msg for w in ("hello", "hi", "hey")):
        return "Hello! I'm your AI assistant running in demo mode. How can I help you today?"
    if "python" in msg:
        return (
            "Python is a versatile, beginner-friendly language widely used for web development, "
            "data science, automation, and AI. Its clean syntax makes it a great first language to learn!"
        )
    if any(w in msg for w in ("what", "how", "why", "explain")):
        return (
            f"Great question about '{message}'! "
            "In a real session the AI would provide a detailed, context-aware answer. "
            "Add an OPENAI_API_KEY to your .env file to enable live responses."
        )
    return (
        f"You said: \"{message}\". "
        "This is a demo response — add an OPENAI_API_KEY to your .env file to get real AI replies."
    )


def load_history():
    if not HISTORY_PATH.exists():
        HISTORY_PATH.write_text("[]")
    try:
        return json.loads(HISTORY_PATH.read_text())
    except Exception:
        HISTORY_PATH.write_text("[]")
        return []


def save_message(role, content):
    history = load_history()
    history.append({"role": role, "content": content})
    HISTORY_PATH.write_text(json.dumps(history, indent=2))


@app.route("/")
def index():
    return render_template("index.html", demo_mode=DEMO_MODE)


@app.route("/api/history")
def api_history():
    return jsonify(load_history())


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "empty message"}), 400

    save_message("user", message)

    if DEMO_MODE:
        reply = fake_reply(message)
        save_message("assistant", reply)
        return jsonify({"reply": reply, "demo": True})

    # Build a concise conversation context (last 10 messages)
    history = load_history()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    for m in history[-10:]:
        messages.append({"role": m["role"], "content": m["content"]})

    try:
        resp = get_client().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        reply = resp.choices[0].message.content.strip()
    except Exception:
        reply = fake_reply(message)
        save_message("assistant", reply)
        return jsonify({"reply": reply, "demo": True})

    save_message("assistant", reply)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
