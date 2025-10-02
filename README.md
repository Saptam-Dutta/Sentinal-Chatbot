# 🤖 Sentinal Chatbot

Sentinal is an AI-powered cybersecurity chatbot built with **Streamlit**, **Ollama**, and **LangChain**.  
It allows you to interact with models like **Mistral** locally while retaining conversation history and providing a chat-like interface.

---

## 🚀 Features
- 💬 Interactive chat UI (messages appear like WhatsApp/Telegram)
- 🧠 Conversation memory (retains previous context)
- ⚡ Powered by [Ollama](https://ollama.ai) with support for **Mistral** and other models
- 📚 Retrieval-Augmented Generation (RAG) with your own documents
- 🎨 Clean and responsive Streamlit interface
- ⏳ Streaming bot responses (word by word typing effect)

---

📂 Project Structure
Cybersecurity_RAG/
data/
   raw/
   cleaned/
indexes/
metadata/
scripts/
   venv/                 # Virtual environment (ignored in Git)
   1_parse_chunk.py   # Load and parse PDFs/docs
   2_build_embeddings.py # Generate embeddings & store in ChromaDB
   3_chatbot.py          # Chatbot interface with Streamlit
requirements.txt
README.md

## 🛠️ Installation(Dont Check the preview goto CODE TAB)

1. Clone this repo
   Terminal:
   git clone https://github.com/SAPTAM-DUTTA/Sentinal-Chatbot.git
   cd Sentinal-Chatbot

3. Create a virtual environment
   Terminal:
   cd ###wherever u have cloned### \Sentinal-Chatbot\scripts
   python -m venv venv
   .\venv\Scripts\activate

5. Install dependencies
   Terminal:
   pip install -r requirements.txt

7. Install Ollama
   Download and install Ollama: https://ollama.ai

8. Pull the Mistral model
   Terminal:
   ollama pull mistral

9. RUN
   python 1_parse_chunk.py
   python 2_build_embeddings.py
   streamlit run 3_chatbot.py
