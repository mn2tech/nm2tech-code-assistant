import streamlit as st
import os, json
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="NM2TECH AI Code Assistant", page_icon="💻", layout="centered")

logo = Image.open("nm2tech_logo.png")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo, use_column_width=False)
    st.markdown("""
        <h1 style='color:#003f63;'>💻 NM2TECH AI Code Assistant</h1>
        <h3 style='font-style:italic; color:#555;'>Technology simplified.</h3>
        <p style='font-size:18px;'>Welcome! Drop in any code snippet and let GPT-4 simplify it.</p>
    """, unsafe_allow_html=True)

# Access tier selector (temporary public control)
plan = st.radio("Select your access tier", ["Free", "Pro", "Admin"])

# Pro banner
st.markdown("""
<div style="padding:10px; background-color:#fff3cd; border-radius:6px; border:1px solid #ffeeba;">
  <strong>🚀 Pro features launching soon:</strong> Debug and Convert options will be fully unlocked for Pro users after launch.
</div>
""", unsafe_allow_html=True)

# Input form
code_input = st.text_area("Paste your code", height=200)
action = st.selectbox("Choose an action", ["Explain", "Debug", "Convert"])
language = st.selectbox("Target Language (if converting)", ["Python", "JavaScript", "C++", "Go"])

# Tier logic
if plan == "Free" and action != "Explain":
    st.warning("Upgrade to Pro to access Debug and Convert features.")
elif st.button("Run Assistant"):
    with st.spinner("Analyzing with GPT-4..."):
        prompt = f"You are a secure code assistant. {action} this code:\n{code_input}"
        if action == "Convert":
            prompt += f"\nConvert it into {language}."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        output = response.choices[0].message.content
        st.markdown("### 💡 Result")
        st.code(output)

        # Optional logging
        log = {"code": code_input, "action": action, "output": output}
        with open("session_logs.json", "a") as f:
            json.dump(log, f)
            f.write("\n")

# Footer
st.markdown("""
---
<center><sub>NM2TECH LLC • Technology simplified.</sub></center>
""", unsafe_allow_html=True)

# Optional styling block
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
    }
    div.stButton > button {
        background-color: #003f63;
        color: white;
        font-size:16px;
        border-radius:6px;
        padding:10px 24px;
    }
    </style>
""", unsafe_allow_html=True)