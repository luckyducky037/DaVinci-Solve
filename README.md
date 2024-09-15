# DaVinci Solve

## Inspiration

Both of us are students who hope to enter the now deflated computer science market, and we shared similar experiences in the mass LeetCode grind. However, we also understood that simply completing LeetCode questions weren't enough; often, potential candidates are met with an unpleasant surprise when they are asked to walk through their thought process. We believed that not being able to communicate your algorithmic ideas was a missed problem, and we hoped to eliminate this with our solution.

## What it does

DaVinci Solve is a way for users to practice communicating their thought process in approaching LeetCode problems (and any other competitive programming problems). This website is an AI-simulated interview scenario which prompts users to outline their solutions to various LeetCode problems through speech and provides feedback on the algorithmic approach they provide.

## How we built it

We used Gradio as a quick front-end and back-end solution. We implemented both Groq and OpenAI APIs for speech-to-text, text-to-speech, and LLM generation. We implemented Leetscrape to scrape problems off of LeetCode, then used Beautiful-Soup to format the problem for display.

We started by mapping out our idea in a flow-chart that we could incrementally complete in order to keep our progress on track. Then we organized our APIs and created a console-based version using various calls from our APIs. Then, we used Gradio to wrap up the functionality in a MVP localhost website.

## Challenges we ran into

There was a good amount of bugs that kept surfacing as we wrote more code, and it was also hard to figure out how to move on with the lacking documentation and flexibility from Gradio.

However, eventually we pulled out the bug spray. With a good amount of perseverance, we finally weeded out every single bug from our code, which provided a good amount of relief.

## Accomplishments that we're proud of

We're pretty proud of being able to go all out on our first hackathon project while spending lots of time for other activities and enjoying the hackathon experience. We even managed to avoid consuming any caffeine and steered away from all-nighters in favour for a good amount of sleep. But definitely the most satisfying thing was getting our project to work in the end.

## What we learned

This was our first hackathon, and it was an eye-opening experience to see how much could happen within 36 hours. We developed skills on building and testing as fast as possible. Lastly, we learned how to cooperate on an exciting project while squeezing out as much fun out of Hack the North as we could.

## What's next for DaVinci Solve

We plan on implementing a better front-end, a memory system for the feedback-giving LLM, and an in-built IDE for users to test their actual code after illustrating their approach.
