import json
import re
from  google import genai
from google.genai import types
import streamlit as st 
from prompts import SYSTEM_PROMPT,WELCOME_MESSAGE_TEMPLATE,SUMMARY_REQUEST_PROMPT
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FROM = st.secrets["TWILIO_WHATSAPP_FROM"]
TWILIO_CONTENT_SID = st.secrets["TWILIO_CONTENT_SID"]

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key = GEMINI_API_KEY)

@st.cache_resource
def get_twilio_client():
    return TwilioClient(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

twilio_client = get_twilio_client()
gemini_client = get_gemini_client()
MODEL_NAME = "gemini-3.5-flash-lite" 

def clean_whatsapp_text(text):
    if not text:
        return "No nutrition summary available."
    text = " ".join(text.split())  # collapse whitespace/newlines
    return text[:1500] + "..." if len(text) > 1500 else text


def whatsapp_address(number, field_name):
    number = number.strip()
    if number.startswith("whatsapp:"):
        number = number[len("whatsapp:"):]
    if not re.fullmatch(r"\+\d{7,15}", number):
        raise ValueError(f"{field_name} must be a phone number in E.164 format, like +14155552671.")
    return f"whatsapp:{number}"


def send_whatsapp(to_number, user_name, summary):
    # Content template expects {{1}} = name, {{2}} = summary.
    try:
        content_sid = TWILIO_CONTENT_SID.strip()
        if not re.fullmatch(r"HX[a-zA-Z0-9]{32}", content_sid):
            return False, "TWILIO_CONTENT_SID must be the complete 34-character SID starting with HX. Copy it from Twilio's Content Template Builder."

        content_variables = json.dumps(
            {"1": user_name, "2": clean_whatsapp_text(summary)}, ensure_ascii=False
        )

        message = twilio_client.messages.create(
            from_=whatsapp_address(TWILIO_WHATSAPP_FROM, "TWILIO_WHATSAPP_FROM"),
            to=whatsapp_address(to_number, "WhatsApp recipient number"),
            content_sid=content_sid,
            content_variables=content_variables,
        )
        return True, message.sid
    except TwilioRestException as error:
        return False, f"Twilio error {error.code}: {error.msg}"
    except Exception as error:
        return False, str(error)






def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role,kind,content):
    st.session_state.messages.append({"role":role,"kind":kind,"content":content})
    render_message(st.session_state.messages[-1]) #render the message in the ui

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text # session_state.chat is an object that we have create using gemini client it will take parts as input and return as text 
    
    except Exception as error:
        return f"sorry, something went wrong: {error}"
    
#step 1 : onboarding(username and phone)
if 'onboarded' not in st.session_state:
    st.title("MacroSnap 🥗")
    st.caption("Snap it. Track it. Text yourself the results.")

    with st.form("onboarding form"):
        name = st.text_input("Your name")
        whatsapp_number = st.text_input(
            "WhatsApp number (with country code)",
            placeholder="+91XXXXXXXXXX",
        )
        
        submitted = st.form_submit_button("Let's go 🚀")

    if submitted:
        if not name.strip() or not whatsapp_number.strip():
            st.warning("please fill in both your name and whatsapp number..")
        else:
            st.session_state.name = name.strip()
            st.session_state.whatsapp_number = whatsapp_number.strip()
            #activate my ai 
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )

            st.session_state.messages = []
            #set the session state as onboarded
            st.session_state.onboarded = True 
            st.rerun()
            #after onboarding stop
    st.stop()


#create chat interface 
header_col, button_col = st.columns([5,2],vertical_alignment="center")
with header_col:
    st.title("🥗 MacroSnap")

with button_col:
    send_disabled = len(st.session_state.messages) <= 2
    if st.button("📤 Send to WhatsApp", disabled=send_disabled, use_container_width=True):
        with st.spinner("Summarizing your day..."):
         summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_whatsapp(st.session_state.whatsapp_number, st.session_state.name, summary)
        if success:
            st.success("Sent! Check your WhatsApp 📲")
        else:
            st.error(f"Couldn't send that: {info}")
            
st.caption(f"Logged in as {st.session_state.name} - updates go to {st.session_state.whatsapp_number}")
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
