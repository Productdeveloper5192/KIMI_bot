
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables (API keys)
load_dotenv()

# Initialize Groq client
client = Groq()
# Use the same model as requested: moonshotai/kimi-k2-instruct
model = "moonshotai/kimi-k2-instruct"

# --- Page Configuration ---
st.set_page_config(
    page_title="Kimi Bot",
    page_icon="🤖",
    layout="centered"
)

# --- Header ---
st.title("🤖 Kimi Bot (Groq)")
st.caption("Powered by Groq & Moonshot AI")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input Handling ---
if prompt := st.chat_input("What is your question?"):
    # 1. Display user message
    st.chat_message("user").markdown(prompt)
    
    # 2. Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Generate and stream assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Create a completion with streaming
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.3,
                max_completion_tokens=4096,
                top_p=1,
                stream=True,
                stop=None,
            )
            
            # Stream the response chunk by chunk
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                message_placeholder.markdown(full_response + "▌")
            
            # Final update without cursor
            message_placeholder.markdown(full_response)
            
            # 4. Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"An error occurred: {e}")
