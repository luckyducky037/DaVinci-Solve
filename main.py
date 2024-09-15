import os

import gradio as gr

from api import API
from fetch import Fetch

api = API()
fetch = Fetch()

question, title, question_body, question_code_stub = None, None, None, None


def handle_first_submission(option):
    global question, title, question_body, question_code_stub

    question_title = option.replace(" ", "-").lower()
    question = fetch.get_question(question_title)

    title = question[0]
    question_body = question[1]
    question_code_stub = question[2]

    return f"{title}\n{question_body}"


def handle_second_submission(audio):
    global question, title, question_body, question_code_stub

    transcript = api.listen(audio, gr=True)
    codegen = api.thinking_to_code(transcript, question_code_stub)
    solution = fetch.get_solution(title)
    compare_result = api.compare_code(solution, codegen, transcript, question_body)

    if compare_result == "Yes":
        title = title.replace(" ", "-").lower()
        feedback = "OK, that approach sounds good. Now, get ready to code it out."
    else:
        feedback = api.evaluate_thinking(solution, codegen, transcript, question_body)

    api.speak(feedback)

    if compare_result == "Yes":
        feedback += f" http://leetcode.com/problems/{title}/description/"

    return transcript, feedback, os.path.abspath("openai_output.wav")


with gr.Blocks() as demo:
    gr.Markdown("# Welcome to DaVinci Solve!")

    text_input = gr.Textbox(
        label="Enter a Leetcode Problem you wish to practice",
        placeholder="Type a Leetcode problem name...",
        lines=1,
    )

    prob_text = gr.Textbox(label="Problem Statement")

    submit_button_1 = gr.Button("Submit Problem")

    dynamic_audio = gr.Audio(
        type="filepath",
        label="Record Your Audio",
        sources=["microphone"],
        visible=False,
    )

    def display_audio():
        return (
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=False, autoplay=False),
        )

    submit_button_2 = gr.Button("Submit Explanation", visible=False)

    transcript = gr.Textbox(label="Transcript", visible=False)
    feedback = gr.Textbox(label="Feedback", visible=False)
    audio_output = gr.Audio(
        value=os.path.abspath("openai_output.wav"),
        type="filepath",
        autoplay=False,
        visible=False,
    )

    submit_button_1.click(
        handle_first_submission,
        inputs=[text_input],
        outputs=[prob_text],
    ).then(
        display_audio,
        inputs=[],
        outputs=[dynamic_audio, submit_button_2, transcript, feedback, audio_output],
    )

    def audio_play():
        return gr.update(
            value=os.path.abspath("openai_output.wav"),
            visible=True,
            autoplay=True,
        )

    submit_button_2.click(
        handle_second_submission,
        inputs=[dynamic_audio],
        outputs=[transcript, feedback, audio_output],
    ).then(
        audio_play,
        inputs=[],
        outputs=[audio_output],
    )


demo.launch(share=True)
