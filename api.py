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


def listen(filename) -> str:
    audio = record_until_silence()
    print(audio)

    wav_data = audio.get_wav_data()

    with open(f"{filename}.wav", "wb") as wav_file:
        wav_file.write(wav_data)

    print(f"WAV file saved as '{filename}.wav'")

    return filename


def groq_listen(filename, prompt="") -> str:
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


def groq_response(
    prompt, temperature: float = 1.0, max_tokens: int | None = None
) -> str:
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return chat_completion.choices[0].message.content


def orca_speak(text: str):
    orca_client.synthesize_to_file(text=text, output_path="orca_output.wav")
    pygame.mixer.music.load("orca_output.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass


class API:
    def __init__(self): ...

    def listen(self) -> str:
        listen("input")
        return groq_listen("input")

    def thinking_to_code(self, leetcode: str, text: str, boilerplate: str) -> str:
        response = groq_response(
            "I am solving the following LeetCode problem:\n\n"
            + leetcode
            + "\n\nHere is my step-by-step thinking for solving the problem:\n\n"
            + text
            + "\n\nHere is the boilerplate code for the problem:\n\n"
            + boilerplate
            + "\n\nPlease follow only my thinking and convert it to code. Please send me just the code and nothing else."
        )
        response = response.strip().strip("```py").strip("```cpp").strip("```").strip()
        return response

    def evaluate_thinking(self, text: str) -> str:
        response = groq_response(
            "Evaluate this explanation from 1-10, with no other output other than the number 1 to 10: "
            + text,
            temperature=0.0,
            max_tokens=1,
        )
        return response

    def compare_code(self, code1: str, code2: str, leetcode: str) -> str:
        response = groq_response(
            'The first code snippet is the solution, the second code snippe is the user\' solution. Compare the following two code snippets and tell me "yes" if they are the same solution and "no" if different:\n\n```\n'
            + code1
            + "\n```\n\n```\n"
            + code2,
            +"\n```\n\n",
            +"Here is the LeetCode problem which the code is solving:\n\n",
            +"```\n" + leetcode + "\n```",
            temperature=0.0,
            max_tokens=1,
        )
        return response

    def speak(self, text: str) -> None:
        orca_speak(text)


api = API()
