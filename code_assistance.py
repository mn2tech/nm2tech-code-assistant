import streamlit as st
import openai, os, json
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Brand visuals
logo = Image.open("nm2tech_logo.png")
st.image(logo, width=120)
st.title("💻 NM2TECH AI Code Assistant")
st.caption("Explain, debug, or convert code securely with GPT-4")

# User input
code_input = st.text_area("Paste your code", height=200)
action = st.selectbox("Choose an action", ["Explain", "Debug", "Convert"])
language = st.selectbox("Target Language (if converting)", ["Python", "JavaScript", "C++", "Go"])

# Trigger assistant
if st.button("Run Assistant"):
    with st.spinner("Analyzing with GPT-4..."):
        prompt = f"You are a secure code assistant. {action} this code:\n{code_input}"
        if action == "Convert":
            prompt += f"\nConvert it into {language}."
        res = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
        output = res.choices[0].message.content
        st.markdown("### 💡 Result")
        st.code(output)

        # Optional logging
        log = {"code": code_input, "action": action, "output": output}
        with open("session_logs.json", "a") as f:
            json.dump(log, f)
            f.write("\n")