import webbrowser
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
    prompt,
    temperature: float = 1.0,
    max_tokens: int | None = None,
    model: str = "llama-3.1-70b-versatile",
) -> str:
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
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


with open("prompts.txt", "r") as f:
    prompts = f.read().splitlines()


class API:
    def __init__(self): ...

    def listen(self) -> str:
        listen("input")
        transcription = groq_listen("input")
        refined = groq_response(
            f"This is the transcription of a voice recording:\n\n{transcription}\n\nPlease refine the words appropriately and return that only. For context, the voice recording was about describing an approach to a coding problem."
        )
        return refined

    def thinking_to_code(self, text: str, boilerplate: str) -> str:
        response = groq_response(
            "\n".join([prompts[0], text, prompts[1], boilerplate, prompts[2]])
        )
        response = (
            response.strip()
            .strip("```python")
            .strip("```py")
            .strip("```cpp")
            .strip("```")
            .strip()
        )
        return response

    def evaluate_thinking(self, code1: str, code2: str, leetcode: str) -> str:
        response = groq_response(
            "\n".join(
                [prompts[3], prompts[4], code1, prompts[6], code2, prompts[7], leetcode]
            ),
            temperature=0.0,
        )
        return response

    def compare_code(self, code1: str, code2: str, leetcode: str) -> str:
        response = groq_response(
            "\n".join(
                [prompts[3], prompts[5], code1, prompts[6], code2, prompts[7], leetcode]
            ),
            temperature=0.0,
            max_tokens=1,
        )
        return response

    def speak(self, text: str) -> None:
        orca_speak(text)

    def open_problem(self, title: str):
        title = title.replace(" ", "-").lower()
        webbrowser.open(f"http://leetcode.com/problems/{title}/description/")


api = API()
api = API()
