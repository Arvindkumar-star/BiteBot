<div align="center">

# 🥗 BiteBot

### Snap your meal. Get a quick nutrition estimate. Send your summary to Telegram.

A lightweight, intelligent Streamlit application that uses **Google Gemini** to estimate calories and macronutrients from meal photos or text descriptions, and delivers conversation summaries straight to your **Telegram Bot**.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=google&logoColor=white)
![Telegram](https://img.shields.io/badge/Messaging-Telegram%20Bot-26A5E4?logo=telegram&logoColor=white)

</div>

---

## 🌟 Features

- **📸 Multimodal Meal Analysis**: Upload meal photos (`JPG`, `JPEG`, `PNG`) or enter text descriptions.
- **⚡ Instant Macro & Calorie Estimation**: Powered by Google Gemini to estimate calories, protein, carbs, and fats in real-time.
- **💬 Interactive Chat Companion**: Ask follow-up questions, adjust serving sizes, or log multiple meals in a single session.
- **📲 Direct Telegram Delivery**: Automatically summarize all meals discussed and receive a structured daily recap directly in your Telegram chat with one click.
- **🛡️ High Availability & Auto-Failover**: Built-in retry mechanism with model fallback to handle temporary API traffic spikes seamlessly.

> *Disclaimer: Nutritional values are AI estimations for general informational use, not medical or clinical dietary advice.*

---

## 🏗️ Architecture & Tech Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **AI & Vision Model**: [Google Gen AI SDK (`google-genai`)](https://ai.google.dev/gemini-api/docs)
- **Messaging Delivery**: [Telegram Bot API](https://core.telegram.org/bots/api)
- **Language**: [Python 3.10+](https://www.python.org/)

---

## 🚀 Quick Start Guide

### 1. Prerequisites

- Python 3.10 or newer
- A **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/))
- A **Telegram Bot Token** (from [@BotFather](https://t.me/BotFather))

### 2. Clone the Repository

```powershell
git clone https://github.com/Arvindkumar-star/BiteBot.git
cd BiteBot
```

### 3. Create & Activate Virtual Environment

```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure Secrets

Create a file named `.streamlit/secrets.toml` in your project root:

```toml
GEMINI_API_KEY = "your-google-gemini-api-key"
TELEGRAM_BOT_TOKEN = "your-bot-token-from-botfather"
```

### 6. Run BiteBot Locally

```powershell
streamlit run app.py
```

---

## 🤖 Setting Up Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts to choose a bot name (e.g. `BiteBot`) and a unique username (ending in `_bot`).
3. Copy the **HTTP API Token** and paste it into `.streamlit/secrets.toml` as `TELEGRAM_BOT_TOKEN`.
4. Open [@userinfobot](https://t.me/userinfobot) on Telegram and click **Start** to get your numeric **Chat ID** (e.g., `123456789`).
5. Open your newly created bot in Telegram and click **Start** so it has permission to send you messages.
6. Enter your Name and Telegram Chat ID in the BiteBot onboarding screen to start tracking!

---

## 📁 Project Structure

```text
bitebot/
├── .streamlit/
│   └── secrets.toml     # Local API credentials (ignored by git)
├── app.py               # Streamlit app, Gemini client, and Telegram delivery logic
├── prompts.py           # System instructions, welcome message, and summary prompts
├── requirements.txt     # Python dependencies
├── spec.md              # Technical specification and channel documentation
└── README.md            # Project documentation
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push your code to GitHub:
   ```bash
   git push origin main
   ```
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and create a new app pointing to your repository `Arvindkumar-star/BiteBot` with `app.py` as the main file.
3. In your app settings on Streamlit Cloud, go to **Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
   ```
4. Click **Save** and your app will deploy instantly!

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
