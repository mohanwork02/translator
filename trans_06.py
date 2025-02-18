import openai
import re
import streamlit as st

# Set OpenAI API Key
api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key  # Set the OpenAI API key

# Function to translate text
def translate_text(text):
    try:
        # Detect language using OpenAI's GPT-4 model
        detection_response = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure you are using the correct model
            messages=[
                {"role": "system", "content": "Detect if the input text is in English or Japanese. Reply with 'english' or 'japanese' only."},
                {"role": "user", "content": text}
            ]
        )
    except openai.error.APIError as e:
        st.error(f"API Error: {e}")
        return ""
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return ""

    detected_language = detection_response["choices"][0]["message"]["content"].strip().lower()

    # Separate Japanese and English text
    japanese_text = re.findall(r'[\u3040-\u30ff\u31f0-\u31ff\u4e00-\u9fff]+', text)
    english_text = re.findall(r'[A-Za-z0-9\s\.,!?]+', text)

    translated_text = ""

    # Translate Japanese to English
    if japanese_text:
        japanese_part = " ".join(japanese_text)
        try:
            japanese_translation_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "Translate the following Japanese text into English."},
                          {"role": "user", "content": japanese_part}]
            )
            translated_text += japanese_translation_response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            st.error(f"Error translating Japanese to English: {e}")

    # Translate English to Japanese
    if english_text:
        english_part = " ".join(english_text)
        try:
            english_translation_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "Translate the following English text into Japanese."},
                          {"role": "user", "content": english_part}]
            )
            if translated_text:
                translated_text += " "
            translated_text += english_translation_response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            st.error(f"Error translating English to Japanese: {e}")

    return translated_text

# Streamlit UI
st.title("Text Translator - English ↔ Japanese")
st.write("Enter your text below to translate between English and Japanese:")

# Input field for text
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

st.session_state.input_text = st.text_area("Input Text", st.session_state.input_text, height=150)

col1, col2 = st.columns(2)
if col1.button("Submit"):
    result = translate_text(st.session_state.input_text)
    st.subheader("Translated Text:")
    st.write(result)
if col2.button("Clear"):
    st.session_state.input_text = ""
    st.experimental_rerun()
