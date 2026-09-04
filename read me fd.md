# 💻 Frontend Dev Chatbot

A Streamlit-based chatbot specialized in frontend development, powered by Google's **Gemini API** (`gemini-3.6-flash`). It only answers questions related to a fixed, allowed tech stack — nothing else.

## Allowed Tech Stack

The assistant is locked to these 5 technologies only:

1. **HTML**
2. **CSS**
3. **JavaScript + Tailwind CSS**
4. **React**
5. **Express**

If you ask about anything outside this stack (Vue, Angular, Python backends, mobile dev, etc.), it will politely redirect you back to the allowed technologies.

## Features

- 🎯 **Scoped expertise** — won't wander into unrelated frameworks or languages
- 🎨 **UI/UX-aware** — defaults to clean, modern, accessible, mobile-first design
- ⚛️ **React best practices** — functional components + hooks only
- 🌊 **Tailwind-first styling** — utility classes over hand-written CSS by default
- 🚀 **Minimal Express guidance** — focused on serving/pairing with the frontend (routes, REST APIs, static files, CORS)
- 💬 **Streaming responses** — answers appear progressively, not all at once
- 🧠 **Chat history** — full conversation kept for the session
- 🗑️ **Clear chat** button in the sidebar to reset the conversation

## Project Structure

```
frontend-dev-chatbot/
├── main.py           # Streamlit app (UI + Gemini API logic)
└── requirement.txt   # Python dependencies
```

## Requirements

- Python 3.9+
- A Google Gemini API key ([console.cloud.google.com](https://console.cloud.google.com) or [aistudio.google.com](https://aistudio.google.com))

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirement.txt
   ```

2. **Set your API key**

   The key is set directly inside `main.py`:

   ```python
   API_KEY = "your-gemini-api-key-here"
   ```

   Replace the placeholder with your own key before running.

3. **Run the app**

   ```bash
   streamlit run main.py
   ```

4. Open the local URL Streamlit prints in your terminal (usually `http://localhost:8501`).

## How It Works

- A detailed **system prompt** in `main.py` instructs the model to stay within the allowed stack and follow specific coding conventions (Tailwind-first, functional React, minimal Express).
- User and assistant messages are stored in `st.session_state.messages` so the conversation persists across turns within a session (resets on page reload or when you click **Clear chat**).
- Each response is streamed from the Gemini API using `chat.send_message(..., stream=True)` and rendered incrementally in the chat window.

## Notes on the API Key

- The key currently lives as a plain string inside `main.py` for convenience — no `.txt` file or environment variable needed.
- Because it's hardcoded, avoid sharing this file publicly (e.g. pushing it to a public GitHub repo) without removing or replacing the key first.
- If you ever need to rotate the key, just update the `API_KEY` variable and restart the app.

## Customizing

- **Change the model**: edit `MODEL_NAME` in `main.py`.
- **Change the allowed stack or rules**: edit the `SYSTEM_PROMPT` string in `main.py`.
- **Change the page title/icon**: edit the `st.set_page_config(...)` call at the top of `main.py`.
