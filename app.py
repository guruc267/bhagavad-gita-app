import streamlit as st
import json
import os

st.set_page_config(page_title="భగవద్గీత", layout="centered")

# Load JSON
with open("data/gita_6_to_10.json", "r", encoding="utf-8") as f:
    gita = json.load(f)

# Load CSS
with open("assets/book.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📘 భగవద్గీత")

# Selection
chapter = st.selectbox(
    "అధ్యాయం ఎంచుకోండి",
    sorted(gita.keys(), key=int),
    format_func=lambda x: f"{x}. {gita[x]['name']}"
)

sloka = st.selectbox(
    "శ్లోకం ఎంచుకోండి",
    sorted(gita[chapter]["slokas"].keys(), key=int)
)

sloka_data = gita[chapter]["slokas"][sloka]
audio_path = sloka_data["audio"]

# Display
st.markdown("### 🕉️ శ్లోకం")
st.write(sloka_data["slokam"])

st.markdown("### 📜 భావం")
st.write(sloka_data["bhavam"])

# Hear (ALL users)
if os.path.exists(audio_path):
    st.audio(audio_path)
else:
    st.info("🔊 రికార్డింగ్ ఇంకా అందుబాటులో లేదు")

# Admin upload
with st.expander("🔐 Admin"):
    admin_key = st.text_input("Admin Key", type="password")

    if admin_key == st.secrets.get("ADMIN_KEY"):
        uploaded = st.file_uploader(
            "🎙️ రికార్డింగ్ అప్లోడ్ చేయండి (.wav)",
            type=["wav", "mp3"]
        )

        if uploaded:
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            with open(audio_path, "wb") as f:
                f.write(uploaded.read())

            st.success("✅ రికార్డింగ్ సేవ్ అయింది")
            st.audio(audio_path)
