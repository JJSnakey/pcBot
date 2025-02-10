import json
import speech_recognition as sr
import requests
import openai
from playsound import playsound

# Configuration
CHARACTER_DETAILS = {
    "name": "Thalor the Wise",
    "background": "An ancient elf wizard with a sharp wit and vast knowledge of arcane lore.",
    "personality": "Sarcastic, wise, but with a soft spot for adventurers in need."
}

CONVERSATION_HISTORY = []

# OpenAI API Configuration
openai.api_key = 'your_openai_api_key'

# Text-to-Speech (TTS) Configuration
TTS_API_KEY = 'your_tts_api_key'
TTS_VOICE_ID = 'custom_voice_id'

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak to Thalor:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return ""

# Function to get AI response from OpenAI API
def get_ai_response(user_input):
    global CONVERSATION_HISTORY
    messages = [
        {"role": "system", "content": f"You are {CHARACTER_DETAILS['name']}, {CHARACTER_DETAILS['background']} with a {CHARACTER_DETAILS['personality']}"},
    ] + CONVERSATION_HISTORY + [{"role": "user", "content": user_input}]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    ai_response = response['choices'][0]['message']['content']
    CONVERSATION_HISTORY.append({"role": "user", "content": user_input})
    CONVERSATION_HISTORY.append({"role": "assistant", "content": ai_response})
    return ai_response

# Function to convert text to speech
def text_to_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{TTS_VOICE_ID}"
    headers = {
        "xi-api-key": TTS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.85
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open('response.mp3', 'wb') as f:
            f.write(response.content)
        playsound('response.mp3')
    else:
        print("Error with TTS API", response.status_code)

# Main loop
def main():
    try:
        while True:
            user_input = recognize_speech()
            if user_input.lower() in ["quit", "exit"]:
                break

            ai_response = get_ai_response(user_input)
            print(f"{CHARACTER_DETAILS['name']}: {ai_response}")
            text_to_speech(ai_response)

    finally:
        # Save conversation history
        with open('conversation_history.json', 'w') as f:
            json.dump(CONVERSATION_HISTORY, f)

if __name__ == "__main__":
    main()
