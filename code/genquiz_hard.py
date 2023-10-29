# get_quiz.py
import json
from typing import Dict

import openai

# I have some chat history saved in a list, where each item is a dictionary representing a message with a role and content.
chat_history = [
    {
        "role": "system",
        "content": "You are a REST API server with an endpoint /generate-random-question, which generates unique primary school level hard difficulty math quiz question about word problems in json data.",
    },
    {"role": "user", "content": "GET /generate-random-question/devops"},
    {
        "role": "assistant",
        "content": '\n\n{\n   "question": "A bakery sold 24 pies in the morning and 18 pies in the evening. If each pie costs $8, how much money did the bakery make from selling pies?",\n    "answer": "336",\n    "explanation": "The bakery sold a total of 24 + 18 = 42 pies. Multiplying 42 by the cost of each pie ($8) gives us a total of $336."\n}',
    },
    {"role": "user", "content": "GET /generate-random-question/jenkins"},
   {
        "role": "assistant",
        "content": '\n\n{\n    "question": "Luke and Olivia have 10 breadsticks, and Luke has 4 times more breadsticks than Olivia. If Paulina takes 1 breadstick from Olivia, how many breadsticks does Olivia have left",\n  "answer": "1",\n    "4x+x =10, 5x=10, x=2. Paulina takes one breadstick so 2-1=1 "\n}',
    },
]

# I define a function that takes a topic string and an API key, and returns a dictionary with a quiz question, options, answer, and explanation.
def get_hard_question(api_key: str) -> Dict[str, str]:
    global chat_history

    # I set the OpenAI API key.
    openai.api_key = api_key

    # I make a copy of the chat history and add the user's message requesting a quiz question for the given topic.
    current_chat = chat_history[:]
    current_user_message = {
        "role": "user",
        "content": f"GET /generate-random-question", 
    }
    current_chat.append(current_user_message)
    chat_history.append(current_user_message)

    # I use the OpenAI API to generate a response based on the current chat history.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=current_chat
    )

    # I extract the quiz question from the response and add it to the chat history as an assistant message.
    quiz = response["choices"][0]["message"]["content"]
    current_assistent_message = {"role": "assistant", "content": quiz}
    chat_history.append(current_assistent_message)

    # I print the quiz question and return it as a dictionary.
    return json.loads(quiz)