<div align="center">

# 🥗 BiteBot

### Snap your meal. Get a quick nutrition estimate. Send your summary to Telegram.

A lightweight Streamlit app that uses Google Gemini to estimate calories and macros from a meal photo or description, then lets you send a conversation summary directly to your Telegram.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=google&logoColor=white)
![Telegram](https://img.shields.io/badge/Messaging-Telegram%20Bot-26A5E4?logo=telegram&logoColor=white)

</div>

---

## What it does

- Accepts a meal photo or a text description.
- Uses Gemini to identify the meal and estimate calories, protein, carbohydrates, and fat.
- Keeps the interaction in an intuitive chat interface.
- Creates a concise meal summary and sends it directly to your Telegram chat.

> Nutrition values are estimates for general informational use, not medical advice.

## Built with

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Google Gen AI SDK](https://ai.google.dev/gemini-api/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Quick start

### 1. Requirements

- Python 3.10 or newer
- A Google Gemini API key
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### 2. Clone and install

```powershell
git clone https://github.com/Arvindkumar-star/bitebot.git
cd bitebot
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 3. Add local secrets

Create `.streamlit/secrets.toml` and add your credentials:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
TELEGRAM_BOT_TOKEN = "your-bot-token-from-botfather"
```

### 4. Run the app

```powershell
streamlit run app.py
```

Enter your name and your Telegram Chat ID (get it from [@userinfobot](https://t.me/userinfobot) or start your bot), chat with BiteBot, and click **Send to Telegram**!
