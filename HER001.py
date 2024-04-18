# Import libraries
import streamlit as st
import requests
from google.cloud import texttospeech
import os

# Replace with your Deep Infra API key
api_key = "gPPAXGBqxZMWShZ1WEOTfjf0hJvCZZ5R"

# Define API endpoint URL
url = "https://api.deepinfra.com/v1/inference/google/gemma-7b-it"

# Create a TTS client
client = texttospeech.TextToSpeechClient()

# Function to convert text to speech using Google Cloud TTS
#def generate_speech(text, voice_name="en-US-Wavenet-A", language_code="en-US"):
#    synthesis_input = texttospeech.SynthesisInput(text=text)
#    voice = texttospeech.VoiceSelectionParams(
#        language_code=language_code, name=voice_name
#    )
#    audio_config = texttospeech.AudioConfig(
#        audio_encoding=texttospeech.AudioEncoding.MP3
#    )
#    response = client.synthesize_speech(
#        input=synthesis_input, voice=voice, audio_config=audio_config
#    )
#    filename = "response.mp3"
#    with open(filename, "wb") as out:
#        out.write(response.audio_content)
#        os.system(f"mpg123 {filename}")  # Or use playsound

# Function to get chatbot response
def get_chatbot_response(prompt):
    payload = {
        "input": prompt,
        "max_new_tokens": 50,  # Adjust as needed
        "temperature": 0.7,    # Adjust as needed
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["results"][0]["generated_text"]
    else:
        return "Error: Unable to get response from chatbot."

# Streamlit app
st.title("My Chatbot App")

# Conversation history
conversation_history = []

# User input
user_message = st.text_input("Enter your message:")

if st.button("Send"):
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # Get chatbot response
    chatbot_response = get_chatbot_response(f"[INST] {user_message} [/INST]")

    # Add chatbot response to conversation history
    conversation_history.append({"role": "assistant", "content": chatbot_response})

    # Display conversation
    for message in conversation_history:
        if message["role"] == "user":
            st.write("You:", message["content"])
        else:
            st.write("Chatbot:", message["content"])
            generate_speech(message["content"])  # Convert response to speech
