import json
import time
import requests
from google import genai
from google.genai import types
import streamlit as st 
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE, SUMMARY_REQUEST_PROMPT

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN", "")

if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN:
    st.error(
        "⚠️ **Missing Secrets on Streamlit Cloud!**\n\n"
        "Please go to your Streamlit App settings -> **Secrets** and add:\n"
        "```toml\n"
        "GEMINI_API_KEY = \"your-gemini-key\"\n"
        "TELEGRAM_BOT_TOKEN = \"your-bot-token\"\n"
        "```"
    )
    st.stop()

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

gemini_client = get_gemini_client()
MODEL_NAME = "gemini-3.5-flash-lite"
FALLBACK_MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]


def send_telegram(chat_id, user_name, summary):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        message_text = f"🥗 BiteBot Summary for {user_name}:\n\n{summary}"
        payload = {
            "chat_id": chat_id.strip(),
            "text": message_text,
        }
        response = requests.post(url, json=payload, timeout=10)
        res_json = response.json()
        if response.status_code == 200 and res_json.get("ok"):
            return True, "Message sent successfully!"
        else:
            description = res_json.get("description", "Failed to send message.")
            return False, f"Telegram error: {description}"
    except Exception as error:
        return False, str(error)


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1]) # render the message in the ui


def ask_gemini(parts):
    # Try with current chat session first, with retry for transient 503s
    for attempt in range(2):
        try:
            return st.session_state.chat.send_message(parts).text 
        except Exception as error:
            error_str = str(error)
            if "503" in error_str or "UNAVAILABLE" in error_str or "429" in error_str:
                time.sleep(1.5)
                continue
            break
    
    # Fallback: if current model failed, attempt backup models
    for fallback_model in FALLBACK_MODELS:
        try:
            # Build conversation contents from session state messages for fallback
            contents = []
            for msg in st.session_state.messages:
                if msg["kind"] == "text":
                    contents.append(msg["content"])
                elif msg["kind"] == "image":
                    contents.append(types.Part.from_bytes(data=msg["content"], mime_type="image/jpeg"))
            if parts:
                contents.extend(parts if isinstance(parts, list) else [parts])
                
            response = gemini_client.models.generate_content(
                model=fallback_model,
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            return response.text
        except Exception:
            continue
            
    return "Sorry, the AI service is experiencing high traffic right now. Please try your message again in a few seconds."
    

# step 1 : onboarding(username and telegram chat id)
if 'onboarded' not in st.session_state:
    st.title("BiteBot 🥗")
    st.caption("Snap it. Track it. Send yourself the results on Telegram.")

    with st.form("onboarding form"):
        name = st.text_input("Your name")
        telegram_chat_id = st.text_input(
            "Telegram Chat ID",
            placeholder="e.g. 123456789",
            help="Get your ID from @userinfobot on Telegram, or start your bot first.",
        )
        
        submitted = st.form_submit_button("Let's go 🚀")

    if submitted:
        if not name.strip() or not telegram_chat_id.strip():
            st.warning("Please fill in both your name and Telegram Chat ID.")
        else:
            st.session_state.name = name.strip()
            st.session_state.telegram_chat_id = telegram_chat_id.strip()
            # activate my ai 
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )

            st.session_state.messages = []
            # set the session state as onboarded
            st.session_state.onboarded = True 
            st.rerun()
    st.stop()


# create chat interface 
header_col, button_col = st.columns([5, 2], vertical_alignment="center")
with header_col:
    st.title("🥗 BiteBot")

with button_col:
    send_disabled = len(st.session_state.messages) <= 2
    if st.button("📤 Send to Telegram", disabled=send_disabled, use_container_width=True):
        with st.spinner("Summarizing your day..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_telegram(st.session_state.telegram_chat_id, st.session_state.name, summary)
        if success:
            st.success("Sent! Check your Telegram 📲")
        else:
            st.error(f"Couldn't send that: {info}")
            
st.caption(f"Logged in as {st.session_state.name} - updates go to Telegram ID: {st.session_state.telegram_chat_id}")
if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)
 
user_input = st.chat_input(
    "Ask a question, or attach a photo of your meal",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append("What is this meal? Give me the calories and macros.")
 
    with st.spinner("Crunching the numbers..."):
        answer = ask_gemini(parts)
    add_message("assistant", "text", answer)
    st.rerun()
