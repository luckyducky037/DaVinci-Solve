import webbrowser
from os import getenv
from pathlib import Path

import speech_recognition as sr
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

from prompts import prompts

load_dotenv()

groq_client = Groq(api_key=getenv("GROQ"))
openai_client = OpenAI(api_key=getenv("OPENAI"))


def record_until_silence():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise. Please wait...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Speak now. Recording will stop after silence is detected.")

        audio = r.listen(source, phrase_time_limit=None, timeout=10)

    return audio


def listen(filename) -> str:
    audio = record_until_silence()

    wav_data = audio.get_wav_data()

    with open(f"{filename}.wav", "wb") as wav_file:
        wav_file.write(wav_data)

    print(f"WAV file saved as '{filename}.wav'")

    return filename


def groq_listen(filename, prompt="") -> str:
    if not filename:
        return
    if filename[-4:] != ".wav":
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
    stop: list[str] = None,
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
        stop=stop,
    )

    return chat_completion.choices[0].message.content


def openai_speak(text: str):
    speech_file_path = Path(__file__).parent / "openai_output.wav"
    response = openai_client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file(speech_file_path)  # TODO: update once fully deprecated


"""
[0]: turn explanation into code
[1]: compare code
[2]: give feedback on code
[3]: refined transcript
"""


class API:
    def listen(self, recording=None, gr: bool = False) -> str:
        if not gr:
            listen("input")
            transcription = groq_listen("input")
        else:
            transcription = groq_listen(recording)
        refined = groq_response(
            prompts[3].format(transcription=transcription), stop=["\n"]
        )
        refined = refined.strip('"')
        return refined

    def thinking_to_code(self, text: str, boilerplate: str) -> str:
        response = groq_response(prompts[0].format(explanation=text, stub=boilerplate))
        response = (
            response.strip()
            .strip("```python")
            .strip("```py")
            .strip("```cpp")
            .strip("```")
            .strip()
        )
        return response

    def evaluate_thinking(
        self, code1: str, code2: str, text: str, leetcode: str
    ) -> str:
        response = groq_response(
            prompts[2].format(
                code1=code1, code2=code2, pseudocode=text, problem=leetcode
            ),
            temperature=0.0,
        )
        return response

    def compare_code(self, code1: str, code2: str, text: str, leetcode: str) -> str:
        response = groq_response(
            prompts[1].format(
                code1=code1, code2=code2, pseudocode=text, problem=leetcode
            ),
            temperature=0.0,
            max_tokens=1,
        )
        return response

    def speak(self, text: str) -> None:
        openai_speak(text)

    def open_problem(self, title: str):
        title = title.replace(" ", "-").lower()
        webbrowser.open(f"http://leetcode.com/problems/{title}/description/")
