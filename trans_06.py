import openai
import re
import streamlit as st

# Set OpenAI API Key
#api_key = st.secrets["OPENAI_API_KEY"]  # Securely retrieve your API key

openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to translate text
def translate_text(text, api_key):
    openai.api_key = api_key

    # Detect the language
    detection_response = openai.ChatCompletion.create(  # Use ChatCompletion correctly
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Detect if the input text is in English or Japanese. Reply with 'english' or 'japanese' only."},
            {"role": "user", "content": text}
        ]
    )
    detected_language = detection_response["choices"][0]["message"]["content"].strip().lower()

    # Separate English and Japanese text using regex
    japanese_text = re.findall(r'[\u3040-\u30ff\u31f0-\u31ff\u4e00-\u9fff]+', text)
    english_text = re.findall(r'[A-Za-z0-9\s\.,!?]+', text)

    # Translate Japanese to English and English to Japanese
    translated_text = ""

    if japanese_text:
        # Translate Japanese to English
        japanese_part = " ".join(japanese_text)
        japanese_translation_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Translate the following Japanese text into English."},
                {"role": "user", "content": japanese_part}
            ]
        )
        translated_text += japanese_translation_response["choices"][0]["message"]["content"].strip()

    if english_text:
        # Translate English to Japanese
        english_part = " ".join(english_text)
        english_translation_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Translate the following English text into Japanese."},
                {"role": "user", "content": english_part}
            ]
        )
        # Add the English-to-Japanese translation
        if translated_text:
            translated_text += " "  # Space to separate the parts
        translated_text += english_translation_response["choices"][0]["message"]["content"].strip()

    return translated_text

# Streamlit UI
st.title("Text Translator - English ↔ Japanese")
st.write("Enter your text below to translate between English and Japanese:")

# Using session_state to hold input_text
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Input field for text
st.session_state.input_text = st.text_area("Input Text", st.session_state.input_text, height=150)

# Buttons for Submit and Clear
col1, col2 = st.columns(2)
if col1.button("Submit"):
    result = translate_text(st.session_state.input_text, api_key)
    st.subheader("Translated Text:")
    st.write(result)
if col2.button("Clear"):
    st.session_state.input_text = ""
    st.experimental_rerun()
