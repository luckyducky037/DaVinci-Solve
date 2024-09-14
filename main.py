from os import getenv

import pvorca
import pygame
import speech_recognition as sr
from dotenv import load_dotenv
from groq import Groq

pygame.mixer.init()
load_dotenv()

groq_client = Groq(api_key=getenv("GROQ"))
orca_client = pvorca.create(access_key=getenv("ORCA"))


def record_until_silence():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise. Please wait...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Speak now. Recording will stop after silence is detected.")

        audio = r.listen(source, phrase_time_limit=None, timeout=None)

    return audio


def listen(filename):
    audio = record_until_silence()
    print(audio)

    wav_data = audio.get_wav_data()

    with open(f"{filename}.wav", "wb") as wav_file:
        wav_file.write(wav_data)

    print(f"WAV file saved as '{filename}.wav'")

    return filename


def groq_listen(filename, prompt=""):
    filename += ".wav"
    with open(filename, "rb") as file:
        transcription = groq_client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="distil-whisper-large-v3-en",
            prompt=prompt,
            response_format="text",
            language="en",
            temperature=0.0,
        )
    return transcription


def groq_response(prompt):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-70b-versatile",
    )

    return chat_completion.choices[0].message.content


def orca_speak(text: str):
    orca_client.synthesize_to_file(text=text, path="orca_output.wav")
    pygame.mixer.music.load("orca_output.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass


transcript = groq_listen(listen("input"))
print(transcript)
response = groq_response(
    "Evaluate this explanation from 1-10, with no other output other than the number 1 to 10: "
    + transcript
)
print(response)
orca_speak(response)
