import streamlit as st
import json
import os
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="భగవద్గీత", layout="centered")

# Load data
with open("data/gita_6_7_8.json", "r", encoding="utf-8") as f:
    gita = json.load(f)

st.title("📘 భగవద్గీత")

# ---- Selection ----
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

# ---- Display text ----
st.markdown("### 🕉️ శ్లోకం")
st.write(sloka_data["slokam"])

st.markdown("### 📜 భావం")
st.write(sloka_data["bhavam"])

audio_path = sloka_data["audio"]

# ---- Hear button (ALL users) ----
if os.path.exists(audio_path):
    st.audio(audio_path)
else:
    st.info("🔊 రికార్డింగ్ ఇంకా అందుబాటులో లేదు")

# ---- ADMIN SECTION ----
with st.expander("🔐 Admin controls"):
    admin_key = st.text_input("Admin key", type="password")

    if admin_key == st.secrets["ADMIN_KEY"]:
        st.success("Admin mode enabled")

        audio_bytes = audio_recorder(
            text="🔴 రికార్డ్ చేయండి",
            recording_color="#e74c3c",
            neutral_color="#95a5a6"
        )

        if audio_bytes:
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)

            st.success("✅ రికార్డింగ్ సేవ్ చేయబడింది")
            st.audio(audio_path)
