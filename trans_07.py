import openai
import os

def translate_text(text, api_key):
    openai.api_key = api_key

    try:
        # Step 1: Detect the language using GPT-4.
        detection_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "Detect if the input text is in English or Japanese. Reply with 'english' or 'japanese' only."
                },
                {"role": "user", "content": text}
            ]
        )
        detected_language = detection_response["choices"][0]["message"]["content"].strip().lower()
        #print(f"[DEBUG] Detected language: {detected_language}")  # Debug output

        # Step 2: Translate based on the detected language.
        if detected_language == "english":
            # Translate from English to Japanese.
            translation_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Translate the following English text into Japanese."},
                    {"role": "user", "content": text}
                ]
            )
            translated_text = translation_response["choices"][0]["message"]["content"].strip()

        elif detected_language == "japanese":
            # Translate from Japanese to English.
            translation_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Translate the following Japanese text into English."},
                    {"role": "user", "content": text}
                ]
            )
            translated_text = translation_response["choices"][0]["message"]["content"].strip()

        else:
            # Fallback for unexpected detection: perform both translations.
            # Translate Japanese to English:
            translation_response_jp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Translate the following Japanese text into English."},
                    {"role": "user", "content": text}
                ]
            )
            translation_jp = translation_response_jp["choices"][0]["message"]["content"].strip()

            # Translate English to Japanese:
            translation_response_en = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Translate the following English text into Japanese."},
                    {"role": "user", "content": text}
                ]
            )
            translation_en = translation_response_en["choices"][0]["message"]["content"].strip()
            
            translated_text = f"English to Japanese: {translation_en}\nJapanese to English: {translation_jp}"

        return translated_text

    except openai.error.OpenAIError as e:
        return f"Error during translation: {str(e)}"

if __name__ == "__main__":
    # Use an environment variable for the API key for security.
    #api_key = os.getenv("OPENAI_API_KEY")
    api_key=""
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    input_text = input("Enter text: ")
    result = translate_text(input_text, api_key)
    print("Translated Text:", result)
