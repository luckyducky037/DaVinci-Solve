from bs4 import BeautifulSoup
from leetscrape import ExtractSolutions, GetQuestion, GetQuestionsList


class Fetch:
    def __init__(self): ...

    def get_question(self, title):
        title = title.replace(" ", "-").lower()
        question = GetQuestion(titleSlug=title).scrape()
        title = question.title
        body = BeautifulSoup(question.Body, "html.parser").get_text()
        code_stub = question.Code
        idx = body.find("Follow-up")
        if idx != -1:
            body = body[:idx]
        idx = body.find("Follow up")
        if idx != -1:
            body = body[:idx]
        return title, body, code_stub

    def get_solution(self, title: str):
        title = title.replace(" ", "-").lower()
        with open(f"solutions/{title}.py") as file:
            return file.read()


fetch = Fetch()

# print(fetch.get_solution("Two Sum"))


# print("\n".join(fetch.get_question("Two Sum")[:2]))
# print("-" * 64)
# print("\n".join(fetch.get_question("Palindrome Number")[:2]))
