<div align="center">

# 🥗 MacroSnap

### Snap your meal. Get a quick nutrition estimate. Send your summary to WhatsApp.

A lightweight Streamlit app that uses Google Gemini to estimate calories and macros from a meal photo or description, then lets you send a conversation summary through Twilio WhatsApp.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=google&logoColor=white)

[![🚀 Live Demo](https://img.shields.io/badge/Live_Demo-Open_MacroSnap-2ea44f?style=for-the-badge)](https://macrosnap-dgemd9ckuqphaqmjuzqeay.streamlit.app/)

</div>

---

## What it does

### [🌐 Try MacroSnap live](https://macrosnap-dgemd9ckuqphaqmjuzqeay.streamlit.app/)

- Accepts a meal photo or a text description.
- Uses Gemini to identify the meal and estimate calories, protein, carbohydrates, and fat.
- Keeps the interaction in a simple chat interface.
- Creates a concise meal summary and sends it to the user's WhatsApp number with Twilio.

> Nutrition values are estimates for general informational use, not medical advice.

## Built with

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Google Gen AI SDK](https://ai.google.dev/gemini-api/docs)
- [Twilio Python SDK](https://www.twilio.com/docs/libraries/python)

## Quick start

### 1. Requirements

- Python 3.10 or newer
- A Google Gemini API key
- A Twilio account with WhatsApp messaging configured

### 2. Clone and install

```powershell
git clone https://github.com/Arvindkumar-star/macrosnap.git
cd macrosnap
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For macOS/Linux, activate the environment with:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### 3. Add local secrets

Create `.streamlit/secrets.toml` and add your own credentials:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
TWILIO_ACCOUNT_SID = "AC..."
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
TWILIO_WHATSAPP_FROM = "+14155238886"
TWILIO_CONTENT_SID = "HX..."
```

Use real values from the **same Twilio account or subaccount** that owns the WhatsApp sender and content template. The app accepts the sender as an E.164 number and adds the `whatsapp:` channel prefix itself.

**Never commit secrets.** `.streamlit/secrets.toml` is excluded by `.gitignore`. If a key or token is accidentally shared or committed, revoke it and create a replacement immediately.

### 4. Configure WhatsApp

For production, register a WhatsApp sender in Twilio and wait until it is ready/online. Create and get WhatsApp approval for a text content template with these numbered placeholders:

- `{{1}}` — the user's name
- `{{2}}` — the meal summary

Set `TWILIO_CONTENT_SID` to that template's full Content SID.

For testing, Twilio's WhatsApp Sandbox requires the recipient to join the Sandbox first. The Sandbox supports its own pre-approved templates; custom content templates require a registered WhatsApp sender.

### 5. Run the app

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, complete the name and WhatsApp number form, then describe a meal or attach a JPG/PNG photo. After chatting, use **Send to WhatsApp** to send the summary.

## Project structure

```text
macrosnap/
├── .streamlit/
│   └── secrets.toml   # Local credentials; do not commit
├── app.py             # Streamlit UI, Gemini requests, and Twilio messaging
├── prompts.py         # Assistant and summary prompts
├── requirements.txt   # Python dependencies
└── README.md
```

## Configuration notes

- The Gemini model is selected by `MODEL_NAME` in `app.py`.
- Phone numbers must use international E.164 format, including the leading `+` and country code.
- WhatsApp templates and senders must belong to the Twilio account/subaccount used by the app.

## Security

Do not put API keys or tokens in source code, screenshots, chat messages, or public repositories. Keep `.streamlit/secrets.toml` local and rotate credentials immediately if exposed.
