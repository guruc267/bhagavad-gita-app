from gtts import gTTS

def generate_audio(text, output_path):
    tts = gTTS(text, lang="te")
    tts.save(output_path)

