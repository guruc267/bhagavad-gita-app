import streamlit as st
import json
import os

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="భగవద్గీత",
    page_icon="📘",
    layout="centered"
)

# -------------------------
# Load CSS (book / mythical UI)
# -------------------------
with open("assets/book.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------
# Load Gita JSON
# -------------------------
with open("data/gita_6_to_10.json", "r", encoding="utf-8") as f:
    gita = json.load(f)

# -------------------------
# App title
# -------------------------
st.markdown("<h1 style='text-align:center;'>📘 భగవద్గీత</h1>", unsafe_allow_html=True)

# -------------------------
# Chapter selection
# -------------------------
chapter_key = st.selectbox(
    "అధ్యాయం ఎంచుకోండి",
    sorted(gita.keys(), key=int),
    format_func=lambda x: f"{x}. {gita[x]['name']}"
)

chapter = gita[chapter_key]
slokas = chapter["slokas"]

# -------------------------
# Sloka selection
# -------------------------
sloka_key = st.selectbox(
    "శ్లోకం ఎంచుకోండి",
    sorted(slokas.keys(), key=int)
)

sloka_data = slokas[sloka_key]
audio_path = sloka_data["audio"]

# -------------------------
# Display Slokam (Sanskrit)
# -------------------------
st.markdown("## 🕉️ శ్లోకం")
st.markdown(
    f"<pre class='slokam-box'>{sloka_data['sanskrit']}</pre>",
    unsafe_allow_html=True
)

# -------------------------
# Telugu Meaning
# -------------------------
st.markdown("## 📖 తెలుగు అర్థం")
st.write(sloka_data["telugu"])

# -------------------------
# Bhavam
# -------------------------
st.markdown("## 📜 భావం")
st.write(sloka_data["bhavam"])

# -------------------------
# Audio playback (for everyone)
# -------------------------
st.markdown("## 🔊 శ్రవణం")
if os.path.exists(audio_path):
    st.audio(audio_path)
else:
    st.info("🔊 ఈ శ్లోకానికి రికార్డింగ్ ఇంకా అందుబాటులో లేదు.")

# -------------------------
# Admin section (upload MP3)
# -------------------------
with st.expander("🔐 Admin (రికార్డింగ్ అప్లోడ్)"):
    admin_key = st.text_input("Admin Key", type="password")

    if admin_key == st.secrets.get("ADMIN_KEY"):
        uploaded_file = st.file_uploader(
            "🎙️ MP3 రికార్డింగ్ అప్లోడ్ చేయండి",
            type=["mp3"]
        )

        if uploaded_file is not None:
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)

            with open(audio_path, "wb") as f:
                f.write(uploaded_file.read())

            st.success("✅ రికార్డింగ్ విజయవంతంగా సేవ్ చేయబడింది.")
            st.audio(audio_path)
    elif admin_key:
        st.error("❌ తప్పు Admin Key")
