thinking_to_code_prompt = """Here is my step-by-step thinking for solving a problem:
{explanation}
Here is the boilerplate code for the problem:
{stub}
Please follow only my thinking and convert it to code. Only follow my thinking. Please write just the code and nothing else."""

compare_code_prompt = """The first code snippet is the solution, the second code snippet is the user's solution.
{code1}
--------------------------------------------------
{code2}
Compare the following two code snippets and write "Yes" if they cover the same edge cases, are both algorithmically correct, and that the second code snippet is at least as fast as the first code snippet. Write "No" if not.
Here is the LeetCode problem which both snippets of code are solving:
{problem}"""

hint_prompt = """The first code snippet is the solution, the second code snippet is derived from the user's explanation.
{code1}
--------------------------------------------------
{code2}
There is something missing from the second code snippet, either logically in that it fails to produce the same output, or that it is too slow with a large time complexity that can be optimized. Give a short hint on what is missing to the user so that they can reiterate. DO NOT write any Python code for the user, but give a verbal hint to lead the user in the right direction. Talk to the user directly, who verbally provided the pseudocode that generated the second code snippet, but limit your hint to at MOST one sentence.
Here is the pseudocode that the user provided:
{pseudocode}
Here is the LeetCode problem which both snippets of code are solving:
{problem}"""

refine_prompt = """This is the transcription of a voice recording:
{transcription}
Please refine the words appropriately and return that only. For context, the voice recording was about describing an approach to a coding problem."""

prompts = [thinking_to_code_prompt, compare_code_prompt, hint_prompt, refine_prompt]
