from api import API
from fetch import Fetch

api = API()
fetch = Fetch()

# Console-based main loop

question_title = input("What question would you like to work on? ")
question_title = question_title.replace(" ", "-").lower()
question = fetch.get_question(question_title)

question_body = question[1]
question_code_stub = question[2]

# Explanation phase
while True:
    print(question[0])
    print("-" * 64)
    print(question_body)

    print("OK, get ready to describe your approach to the question.")

    transcript = api.listen()
    print("transcript:", transcript)
    codegen = api.thinking_to_code(transcript, question_code_stub)
    print("codegen:", codegen)
    solution = fetch.get_solution(question_title)
    print("solution:", solution)
    compare_result = api.compare_code(solution, codegen, question_body)
    print(compare_result)

    if compare_result == "Yes":
        print("OK, that approach sounds good. Now, get ready to code it out.")
        break
    else:
        print(api.evaluate_thinking(solution, codegen, question_body))

# Implementation phase
