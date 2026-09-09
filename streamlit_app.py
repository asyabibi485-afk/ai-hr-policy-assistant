import streamlit as st
from google import genai
import os

st.set_page_config(
    page_title="AI HR Policy Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI HR Policy Assistant")
st.caption("Ask questions about company HR policies")

api_key = st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)


def load_policy():
    with open(
        "policies/hr_policy.txt",
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def ask_gemini(question):

    policy = load_policy()

    prompt = f"""
You are an AI HR Policy Assistant.

Answer the employee's question using the HR policy below.

Do not invent information.

If the answer is not available in the policy,
say that the information is not available and
recommend contacting HR.

HR POLICY:
{policy}

QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input(
    "Ask your HR policy question..."
)


if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    answer = ask_gemini(question)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)
