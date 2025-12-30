import streamlit as st
import json
import os
import base64

# -------------------------------------------------
# Page config (MUST be first Streamlit call)
# -------------------------------------------------
st.set_page_config(
    page_title="భగవద్గీత",
    page_icon="📘",
    layout="centered"
)

# -------------------------------------------------
# Background image (Krishna / Peacock Feather)
# -------------------------------------------------
def add_bg_from_local(image_file):
    ext = image_file.split(".")[-1]

    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
              linear-gradient(
                rgba(0,0,0,0.82),
                rgba(0,0,0,0.82)
              ),
              url("data:image/{ext};base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ⚠️ Make sure this file exists
add_bg_from_local("assets/krishna_bg.webp")

# -------------------------------------------------
# Session state (book-style page turning)
# -------------------------------------------------
if "sloka_index" not in st.session_state:
    st.session_state.sloka_index = 0

if "last_chapter" not in st.session_state:
    st.session_state.last_chapter = None

# -------------------------------------------------
# Load Book / Temple CSS
# -------------------------------------------------
with open("assets/book.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------------------------
# ✨ Divine Glow + Lamp Animation (MUST be after book.css)
# -------------------------------------------------
st.markdown(
    """
    <style>
    h1, h2, h3 {
      color: #f6e7b2 !important;
      text-shadow:
        0 0 6px rgba(255, 215, 120, 0.45),
        0 0 14px rgba(255, 180, 60, 0.35) !important;
    }

    .slokam-box {
      color: #fff4cc !important;
      text-shadow:
        0 0 10px rgba(255, 220, 150, 0.5) !important;
    }

    p {
      text-shadow:
        0 0 4px rgba(255, 200, 120, 0.25) !important;
    }

    @keyframes diyaGlow {
      0% {
        box-shadow:
          inset 0 0 120px rgba(255, 180, 80, 0.06),
          inset 0 0 220px rgba(255, 140, 40, 0.05);
      }
      50% {
        box-shadow:
          inset 0 0 180px rgba(255, 200, 90, 0.10),
          inset 0 0 320px rgba(255, 150, 60, 0.08);
      }
      100% {
        box-shadow:
          inset 0 0 120px rgba(255, 180, 80, 0.06),
          inset 0 0 220px rgba(255, 140, 40, 0.05);
      }
    }

    .stApp {
      animation: diyaGlow 7s ease-in-out infinite !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Load Gita JSON
# -------------------------------------------------
gita = {}

with open("data/gita_6_to_10.json", "r", encoding="utf-8") as f:
    gita.update(json.load(f))

if os.path.exists("data/gita_7.json"):
    with open("data/gita_7.json", "r", encoding="utf-8") as f:
        gita.update(json.load(f))

# -------------------------------------------------
# App Title
# -------------------------------------------------
st.markdown("<h1 style='text-align:center;'>📘 భగవద్గీత</h1>", unsafe_allow_html=True)

# -------------------------------------------------
# Chapter Selection
# -------------------------------------------------
chapter_key = st.selectbox(
    "అధ్యాయం ఎంచుకోండి",
    sorted(gita.keys(), key=int),
    format_func=lambda x: f"{x}. {gita[x]['name']}"
)

if st.session_state.last_chapter != chapter_key:
    st.session_state.sloka_index = 0
    st.session_state.last_chapter = chapter_key

chapter = gita[chapter_key]
slokas = chapter["slokas"]

# -------------------------------------------------
# Sloka Navigation
# -------------------------------------------------
sloka_keys = sorted(slokas.keys(), key=int)
sloka_key = sloka_keys[st.session_state.sloka_index]
sloka_data = slokas[sloka_key]
audio_path = sloka_data.get("audio", "")

# -------------------------------------------------
# Slokam
# -------------------------------------------------
st.markdown("## 🕉️ శ్లోకం")
st.markdown(
    f"<pre class='slokam-box'>{sloka_data['sanskrit']}</pre>",
    unsafe_allow_html=True
)

# -------------------------------------------------
# Telugu Meaning
# -------------------------------------------------
st.markdown("## 📖 తెలుగు అర్థం")
st.write(sloka_data["telugu"])

# -------------------------------------------------
# Bhavam
# -------------------------------------------------
st.markdown("## 📜 భావం")
st.write(sloka_data["bhavam"])

# -------------------------------------------------
# Audio Playback
# -------------------------------------------------
st.markdown("## 🔊 శ్రవణం")
if audio_path and os.path.exists(audio_path):
    st.audio(audio_path)
else:
    st.info("🔊 ఈ శ్లోకానికి రికార్డింగ్ ఇంకా అందుబాటులో లేదు.")

# -------------------------------------------------
# Page Turn Controls
# -------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ ముందు") and st.session_state.sloka_index > 0:
        st.session_state.sloka_index -= 1
        st.rerun()

with col2:
    st.markdown(
        f"<p style='text-align:center;'>శ్లోకం {sloka_key} / {len(sloka_keys)}</p>",
        unsafe_allow_html=True
    )

with col3:
    if st.button("తర్వాత ➡️") and st.session_state.sloka_index < len(sloka_keys) - 1:
        st.session_state.sloka_index += 1
        st.rerun()

# -------------------------------------------------
# Admin Section (Audio Upload)
# -------------------------------------------------
with st.expander("🔐 Admin (రికార్డింగ్ అప్లోడ్)"):
    admin_key = st.text_input("Admin Key", type="password")

    if admin_key == st.secrets.get("ADMIN_KEY"):
        uploaded_file = st.file_uploader("🎙️ MP3 అప్లోడ్ చేయండి", type=["mp3"])
        if uploaded_file and audio_path:
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            with open(audio_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success("✅ రికార్డింగ్ సేవ్ అయ్యింది")
            st.audio(audio_path)
    elif admin_key:
        st.error("❌ తప్పు Admin Key")
