import streamlit as st
import json
import os
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="భగవద్గీత", layout="centered")

# ---------- Load data ----------
with open("data/gita_6_to_10.json", "r", encoding="utf-8") as f:
    gita = json.load(f)

# ---------- Load CSS ----------
with open("assets/book.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📘 భగవద్గీత")

# ---------- Selection ----------
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
audio_path = sloka_data.get("audio", "")

# ---------- Display ----------
st.markdown("### 🕉️ శ్లోకం")
st.write(sloka_data["slokam"])

st.markdown("### 📜 భావం")
st.write(sloka_data["bhavam"])

# ---------- Hear (Everyone) ----------
if audio_path and os.path.exists(audio_path):
    st.markdown("### 🔊 వినండి")
    st.audio(audio_path)
else:
    st.info("🔊 రికార్డింగ్ ఇంకా అందుబాటులో లేదు")

# ---------- Admin Section ----------
with st.expander("🔐 Admin"):
    admin_key = st.text_input("Admin Key", type="password")

    if admin_key == st.secrets.get("ADMIN_KEY"):
        st.success("Admin Mode Enabled")

        audio_bytes = audio_recorder(
            text="🔴 రికార్డ్ చేయండి",
            recording_color="#b22222",
            neutral_color="#d4af37"
        )

        if audio_bytes:
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)

            st.success("✅ రికార్డింగ్ సేవ్ చేయబడింది")
            st.audio(audio_path)
