import streamlit as st
import os, json
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
from pyairtable import Table
from datetime import datetime

# ✅ Session setup
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(datetime.utcnow().timestamp())

if "pro_uses_left" not in st.session_state:
    st.session_state["pro_uses_left"] = 10  # 🎟️ Free Pro trial tokens

# ✅ Airtable logging
def log_to_airtable(user, prompt, response, feedback):
    table = Table(
        st.secrets["AIRTABLE_API_KEY"],
        st.secrets["AIRTABLE_BASE_ID"],
        "Logs"
    )
    table.create({
        "Timestamp": datetime.utcnow().isoformat(),
        "User": user,
        "Prompt": prompt,
        "Response": response,
        "Feedback": feedback
    })

# ✅ Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ App config
st.set_page_config(page_title="NM2TECH AI Code Assistant", page_icon="💻", layout="centered")

# ✅ Branding
logo = Image.open("nm2tech_logo.png")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo, use_container_width=False)
    st.markdown("""
        <h1 style='color:#003f63;'>💻 NM2TECH AI Code Assistant</h1>
        <p style='font-size:18px;'>Welcome! Drop in any code snippet and let GPT-4 simplify it.</p>
    """, unsafe_allow_html=True)

# 🔘 Tier selector
tier = st.radio("Select your access tier:", ["Free", "Pro"], horizontal=True)

query_params = st.query_params
if query_params.get("tier", "free") == "pro" and st.session_state["pro_uses_left"] == 10:
    st.markdown("""
    <div style="margin-top:10px; padding:16px; background-color:#e6ffe6; border:1px solid #28a745; border-radius:8px;">
      <h4 style='margin-bottom:10px;'>✅ Upgrade Confirmed</h4>
      <p style='font-size:16px;'>Thanks for subscribing to <strong>NM2TECH Pro</strong>! You've unlocked unlimited access to Debug, Convert, and future premium features.</p>
      <p style='font-size:16px;'>Let’s build something incredible together 💻✨</p>
    </div>
    """, unsafe_allow_html=True)

# 💳 Conditional Pro banner
if tier == "Pro":
    st.markdown("""
    <div style="margin-top:10px; padding:16px; background-color:#f8f9fa; border:1px solid #dee2e6; border-radius:8px;">
      <h4 style='margin-bottom:10px;'>💸 NM2TECH Pro Plan</h4>
      <p style='font-size:16px;'>Unlimited runs · Debug & Convert · Priority support</p>
      <p style='font-size:16px;'>Only <strong>$9.99/month</strong></p>
      <a href="https://buy.stripe.com/00w9AS21ney60zs1cvdZ603" target="_blank"
         style="color:white; background-color:#0077cc; padding:10px 20px; text-decoration:none; border-radius:6px; display:inline-block;">
         🔓 Upgrade to Pro
      </a>
    </div>
    """, unsafe_allow_html=True)

# 📢 Announcement
st.markdown("""
<div style="padding:10px; background-color:#fff4e5; border-radius:6px; border:1px solid #ffeeba;">
  <strong>🔐 Public preview complete:</strong> Debug and Convert features are now exclusive to Pro users. Select “Pro” to access your free trial. Subscription required once trial ends.
</div>
""", unsafe_allow_html=True)

# ✅ Input form
code_input = st.text_area("Paste your code", height=200)
action = st.selectbox("Choose an action", ["Explain", "Debug", "Convert"])
language = st.selectbox("Target Language (if converting)", ["Python", "JavaScript", "C++", "Go"])

# 🔐 Gating logic with trial tracking
if tier == "Free" and action != "Explain":
    st.warning("Upgrade to Pro to access Debug and Convert features.")
elif tier == "Pro" and action != "Explain":
    if st.session_state["pro_uses_left"] > 0:
        st.info(f"🎟️ {st.session_state['pro_uses_left']} free Pro runs left")
    else:
        st.error("🚫 Free Pro trial complete — please subscribe to continue.")
        st.stop()

# ✅ Assistant logic
# ✅ Assistant logic
if st.button("Run Assistant"):
    with st.spinner("Analyzing with GPT-4..."):
        # 🔧 Enhanced prompt template
        prompt = f"""
        You're a secure AI code assistant built for the NM2TECH platform.

        Task: {action}
        Language Preference: {language}

        Instructions:
        - If explaining, clearly describe the logic and purpose of the code.
        - If debugging, identify and fix any issues while explaining your changes.
        - If converting, rewrite the code accurately in {language} using best practices.

        Code:
        {code_input}

        Return only your response or converted code as text.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        output = response.choices[0].message.content
        st.markdown("### 💡 Result")
        st.code(output)

        # ✅ Feedback + Airtable logging
        feedback = st.radio("Was this result helpful?", ["👍 Yes", "👎 No"], horizontal=True)

        log_to_airtable(
            user=st.session_state["session_id"],
            prompt=prompt,
            response=output,
            feedback=feedback
        )

        # ✅ Local logging
        with open("session_logs.json", "a") as f:
            json.dump({"code": code_input, "action": action, "output": output}, f)
            f.write("\n")

        # 🎟️ Token deduction
        if tier == "Pro" and action != "Explain":
            st.session_state["pro_uses_left"] -= 1

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
    }
    h1 { color: #002b5b; font-size: 28px; }
    p { color: #444444; }
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
    .stRadio > div { color: #002b5b; font-weight: 500; }
    .stSelectbox, .stTextArea {
        border-radius: 6px;
        font-size: 15px;
    }
    </style>
""", unsafe_allow_html=True)