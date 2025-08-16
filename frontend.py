
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Career Coach (Groq)", layout="wide")
st.title("💼 Career Navigator — AI Job & Career Coach")

with st.sidebar:
    st.header("What it can do")
    st.markdown(
        "- Career advice\n"
        "- Resume rewrite\n"
        "- Interview questions\n"
        "- Networking outreach (simulated)"
    )
    st.caption("Tip: Try: 'Rewrite my resume for a Data Analyst role' or 'Generate 10 PM interview questions'.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("What career question can I help with today?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    try:
        response = requests.post(BACKEND_URL, json={"message": user_input}, timeout=120)
        payload = response.json()
        tool = payload.get("tool_called", "None")
        answer = payload.get("response", "Sorry, I couldn't generate a response.")
        st.session_state.chat_history.append(
            {"role": "assistant", "content": f"{answer}\n\n_Used Tool:_ **{tool}**"}
        )
    except Exception:
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "⚠️ Backend not reachable. Start the API server at http://localhost:8000"}
        )

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
