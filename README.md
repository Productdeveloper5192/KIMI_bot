# Kimi Bot

A minimal Streamlit chat interface for Moonshot AI's **Kimi K2** model, served through Groq's low-latency inference API with token-by-token streaming.

## What It Does

- Provides a chat UI (Streamlit) where the user talks to `moonshotai/kimi-k2-instruct`.
- Keeps the full conversation in session state and replays it on every turn, so the model has multi-turn context, not just the latest message.
- Streams the response back token-by-token as it's generated, rather than waiting for the full reply.

## End-to-End Flow

```
 User types a message in the Streamlit chat box
        │
        ▼
 st.session_state.messages   ← full conversation history is appended here
        │
        ▼
 Groq client.chat.completions.create(
     model="moonshotai/kimi-k2-instruct",
     messages=<entire history>,
     stream=True
 )
        │
        ▼
 Response streams back chunk by chunk; each chunk's text is appended
 and re-rendered live in the chat bubble (with a "▌" cursor while
 still generating)
        │
        ▼
 Final response is stored back into session_state.messages,
 so the next turn's request includes it as context
```

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Inference | Groq API (`moonshotai/kimi-k2-instruct`) |
| Config | `python-dotenv` |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Groq API key
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key
```
(Get a key from [console.groq.com](https://console.groq.com/keys).)

### 3. Run it
```bash
streamlit run KIMI.py
```
Open the URL Streamlit prints (typically `http://localhost:8501`) and start chatting.
