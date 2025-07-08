import streamlit as st
import os, json
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
from pyairtable import Table
from datetime import datetime

# ✅ Session ID logic
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(datetime.utcnow().timestamp())

# ✅ Airtable logging function
def log_to_airtable(user, prompt, response):
    table = Table(
        st.secrets["AIRTABLE_API_KEY"],
        st.secrets["AIRTABLE_BASE_ID"],
        "Logs"
    )
    table.create({
        "Timestamp": datetime.utcnow().isoformat(),
        "User": user,
        "Prompt": prompt,
        "Response": response
    })

# ✅ Load environment and API
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ UI config and branding
st.set_page_config(page_title="NM2TECH AI Code Assistant", page_icon="💻", layout="centered")

logo = Image.open("nm2tech_logo.png")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo, use_container_width=False)
    st.markdown("""
        <h1 style='color:#003f63;'>💻 NM2TECH AI Code Assistant</h1>
        <p style='font-size:18px;'>Welcome! Drop in any code snippet and let GPT-4 simplify it.</p>
    """, unsafe_allow_html=True)

# ✅ Access tier logic
plan = st.radio("Select your access tier", ["Free", "Pro"])

st.markdown("""
<div style="padding:10px; background-color:#d1ecf1; border-radius:6px; border:1px solid #bee5eb;">
  <strong>🌟 All features now live:</strong> Enjoy full access to Explain, Debug, and Convert functions during our public launch. Pricing tier enforcement begins soon!
</div>
""", unsafe_allow_html=True)

# ✅ Input form
code_input = st.text_area("Paste your code", height=200)
action = st.selectbox("Choose an action", ["Explain", "Debug", "Convert"])
language = st.selectbox("Target Language (if converting)", ["Python", "JavaScript", "C++", "Go"])

# ✅ Assistant logic
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

        # Add feedback option
        feedback = st.radio("Was this result helpful?", ["👍 Yes", "👎 No"], horizontal=True)


        # ✅ Log this interaction
        log_to_airtable(
            user=st.session_state["session_id"],
            prompt=prompt,
            response=output
            feedback=feedback  # New argument!
        )

        # Optional local logging
        log = {"code": code_input, "action": action, "output": output}
        with open("session_logs.json", "a") as f:
            json.dump(log, f)
            f.write("\n")

# ✅ Footer
st.markdown("""
---
<center><sub>NM2TECH LLC • Technology simplified.</sub></center>
""", unsafe_allow_html=True)

# ✅ Custom styling
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        color: #1f1f1f;
        padding: 0px;
        margin: 0px;
    }
    h1 {
        color: #002b5b;
        font-size: 28px;
    }
    p {
        color: #444444;
    }
    div.stButton > button {
        background-color: #0077cc;
        color: #ffffff;
        font-size:16px;
        border-radius:8px;
        padding:12px 28px;
        border: none;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #005fa3;
    }
    .stRadio > div {
        color: #002b5b;
        font-weight: 500;
    }
    .stSelectbox, .stTextArea {
        border-radius: 6px;
        font-size: 15px;
    }
    </style>
""", unsafe_allow_html=True)