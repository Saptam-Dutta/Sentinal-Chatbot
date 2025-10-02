import streamlit as st
import subprocess
import shutil
import sys
import ollama

# ==============================
# CONFIG
# ==============================
MODEL_NAME = "mistral"

# ==============================
# HELPER: Ensure Ollama & Model
# ==============================
def ensure_ollama_and_model(model_name):
    if shutil.which("ollama") is None:
        st.error("❌ Ollama is not installed. Please install it from https://ollama.ai")
        sys.exit(1)

    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        if model_name not in result.stdout:
            st.write(f"⬇️ Pulling model '{model_name}' ...")
            subprocess.run(["ollama", "pull", model_name], check=True)
            st.success(f"✅ Model '{model_name}' pulled successfully.")
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Error checking or pulling model: {e}")
        sys.exit(1)

# Ensure model is ready
ensure_ollama_and_model(MODEL_NAME)

# ==============================
# STREAMLIT UI
# ==============================
st.set_page_config(page_title="Sentinal", page_icon="🤖", layout="centered")
st.title("💬 I am Sentinal... Ask me Anything >>> About Cybersecurity")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ==============================
# DISPLAY CHAT HISTORY
# ==============================
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style='text-align: right; background-color: #DCF8C6; color: #000; 
        padding: 12px; border-radius: 10px; margin: 5px 0; 
        display: inline-block; max-width: 70%; font-size: 15px; line-height: 1.5;'>
        {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align: left; background-color: #EDEDED; color: #000; 
        padding: 12px; border-radius: 10px; margin: 5px 0; 
        display: inline-block; max-width: 70%; font-size: 15px; line-height: 1.5;'>
        🤖 {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# ==============================
# INPUT FORM
# ==============================
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("Type your message:", "")
    submitted = st.form_submit_button("Send")

# ==============================
# PROCESS INPUT + STREAM REPLY
# ==============================
if submitted and user_query.strip():
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_query})

    # Show query instantly
    with st.chat_message("user"):
        st.markdown(user_query)

    # Create placeholder for bot reply (will fill in word by word)
    bot_placeholder = st.empty()
    bot_text = ""

    try:
        # Streaming reply from Ollama
        for chunk in ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]],
            stream=True
        ):
            token = chunk["message"]["content"]
            bot_text += token
            bot_placeholder.markdown(f"""
            <div style='text-align: left; background-color: #EDEDED; color: #000; 
            padding: 12px; border-radius: 10px; margin: 5px 0; 
            display: inline-block; max-width: 70%; font-size: 15px; line-height: 1.5;'>
            🤖 {bot_text}
            </div>
            """, unsafe_allow_html=True)

        # Save final reply
        st.session_state["messages"].append({"role": "assistant", "content": bot_text})
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error communicating with Ollama: {e}")
