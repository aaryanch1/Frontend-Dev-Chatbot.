import os
import streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------
# Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Frontend Dev Chatbot",
    page_icon="💻",
    layout="wide",
)

MODEL_NAME = "gemini-3.6-flash"
API_KEY = "enter your key here"

SYSTEM_PROMPT = """You are "FrontendGPT", a specialized frontend development assistant.

STRICT SCOPE — you only help with:
1. HTML
2. CSS
3. JavaScript + Tailwind CSS
4. React
5. Express (Node.js backend that serves/pairs with the frontend)

RULES:
- You ONLY write code, explain concepts, debug, and give UI/UX advice using the 5 technologies above.
- Do NOT use or recommend other frameworks/libraries (no Vue, Angular, Svelte, Bootstrap, jQuery, Django, Flask, PHP, etc.) unless the user explicitly says they only want a comparison — even then, steer back to the allowed stack.
- If a user asks for something outside this scope (e.g. mobile apps in Swift, Python data science, etc.), politely explain that you're specialized in HTML/CSS/Tailwind/JS/React/Express and offer to help with the frontend-related part of their request instead.
- When writing UI/UX, prefer clean, modern, accessible design: sensible spacing, responsive layouts (mobile-first), semantic HTML, Tailwind utility classes, and good color/contrast choices.
- When code is requested, output complete, runnable code blocks with correct file names/extensions (.html, .css, .jsx, .js) and brief setup instructions (e.g. npm commands) when relevant.
- For React, assume functional components + hooks (no class components) unless asked otherwise.
- For styling, default to Tailwind CSS utility classes rather than hand-written CSS, unless the user asks for plain CSS specifically.
- For backend/API needs, use Express (Node.js) only — keep it minimal and focused on serving the frontend (routes, REST APIs, static file serving, CORS, etc.).
- Keep explanations concise and practical; favor working examples over long theory.
"""

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.title("💻 Frontend Dev Chatbot")
    st.markdown(
        "This assistant only helps with:\n"
        "- **HTML**\n"
        "- **CSS**\n"
        "- **JavaScript + Tailwind**\n"
        "- **React**\n"
        "- **Express**\n"
    )
    st.divider()

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------
# Resolve API key
# ---------------------------------------------------------
api_key = API_KEY

if not api_key:
    st.warning("No API key set. Add your key to the API_KEY variable in main.py.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)

# ---------------------------------------------------------
# Chat state
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user"/"assistant", "content": str}

st.header("💻 Frontend Dev Chatbot")
st.caption("Ask for UI/UX, components, layouts, or code — HTML · CSS · Tailwind · JS · React · Express only.")

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------
prompt = st.chat_input("Describe the UI, component, or bug you need help with...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            # Build Gemini-style history (everything except the latest prompt)
            gemini_history = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [m["content"]]})

            chat = model.start_chat(history=gemini_history)
            response_stream = chat.send_message(prompt, stream=True)

            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Error calling the API: {e}"
            placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
