# import gradio as gr

# from api import API

# api = API()


# def main(audio, option):
#     transcript = api.listen(audio, gr=True)

#     return transcript


# with gr.Blocks() as demo:
#     gr.Markdown("# Welcome to DaVinci Solve!")

#     text_input = gr.Textbox(
#         label="Enter a Leetcode Problem you wish to practice",
#         placeholder="Type a Leetcode problem name...",
#         lines=1,
#     )

#     output_text = gr.Textbox(label="Output Text")

#     mic_input = gr.Audio(
#         type="filepath", label="Record Your Audio", sources=["microphone"]
#     )

#     submit_button = gr.Button("Submit")

#     submit_button.click(main, inputs=[mic_input, text_input], outputs=[output_text])

# demo.launch(share=True)

import gradio as gr

from api import API
from fetch import Fetch

api = API()
fetch = Fetch()

# question, title, question_body, question_code_stub = (
#     gr.State(None),
#     gr.State(None),
#     gr.State(None),
#     gr.State(None),
# )

question, title, question_body, question_code_stub = None, None, None, None

# Function to handle the first submission (problem submission)
def handle_first_submission(option, stage):
    global question, title, question_body, question_code_stub

    question_title = option.replace(" ", "-").lower()
    question = fetch.get_question(question_title)

    title = question[0]
    question_body = question[1]
    question_code_stub = question[2]

    transcript = f"{title}\n{question_body}"
    stage = 1  # Move to stage 1 to display the audio component
    return transcript, stage


# Function to handle the second submission (audio recording submission)
def handle_second_submission(audio, option):
    global question, title, question_body, question_code_stub

    transcript = api.listen(audio, gr=True)
    codegen = api.thinking_to_code(transcript, question_code_stub)
    solution = fetch.get_solution(title)
    compare_result = api.compare_code(solution, codegen, question_body)

    if compare_result == "Yes":
        title = title.replace(" ", "-").lower()
        feedback = f"OK, that approach sounds good. Now, get ready to code it out. http://leetcode.com/problems/{title}/description/"
        # api.speak(feedback)
    else:
        feedback = api.evaluate_thinking(solution, codegen, question_body)
        # api.speak(feedback)

    print(transcript)

    return feedback

# Create the Gradio interface
with gr.Blocks() as demo:
    # question, title, question_body, question_code_stub = (
    #     gr.State(None),
    #     gr.State(None),
    #     gr.State(None),
    #     gr.State(None),
    # )

    gr.Markdown("# Welcome to DaVinci Solve!")

    # Textbox for Leetcode problem input
    text_input = gr.Textbox(
        label="Enter a Leetcode Problem you wish to practice",
        placeholder="Type a Leetcode problem name...",
        lines=1,
    )

    # Output text area for displaying results
    prob_text = gr.Textbox(label="Problem Statement")

    # State to track the submission stage
    stage = gr.State(value=0)

    submit_button_1 = gr.Button("Submit Problem")

    # Placeholder for dynamic audio component
    dynamic_audio = gr.Audio(
        type="filepath",
        label="Record Your Audio",
        sources=["microphone"],
        visible=False,
    )

    # Function to display the audio component dynamically based on the stage
    def display_audio(stage):
        if stage == 1:
            return gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    # Submit button for the first and second stages
    submit_button_2 = gr.Button("Submit Explanation", visible=False)

    # Output text area for displaying results
    feedback = gr.Textbox(label="Feedback", visible=False)

    # First click: handle problem submission, show audio input
    submit_button_1.click(
        handle_first_submission,
        inputs=[text_input, stage],
        outputs=[prob_text, stage],
    ).then(display_audio, inputs=[stage], outputs=[dynamic_audio, submit_button_2, feedback])

    # Second click: handle audio submission (after it's visible)
    submit_button_2.click(
        handle_second_submission,
        inputs=[dynamic_audio, text_input],
        outputs=[feedback],
    )


# Launch the Gradio app
demo.launch(share=True)
