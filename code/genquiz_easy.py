# get_quiz.py
import json
from typing import Dict

import openai

# I have some chat history saved in a list, where each item is a dictionary representing a message with a role and content.
chat_history = [
    {
        "role": "system",
        "content": "You are a REST API server with an endpoint /generate-random-question, which generates unique primary school easy level math quiz question about addtion, subtraction and multiplication in json data.",
    },
    {"role": "user", "content": "GET /generate-random-question/devops"},
    {
        "role": "assistant",
        "content": '\n\n{\n    "question": "What is the 10%2 equal to?",\n "answer": "5",\n    "explanation": "If you have 10 pencils that you need to allocate across 2 people equally, you give each person 5 pencils"\n}',
    },
    {"role": "user", "content": "GET /generate-random-question/jenkins"},
    {
        "role": "assistant",
        "content": '\n\n{\n    "question": "If Mary has 10 apples, and Tracy has 3 more apples than Mary. How many apples does Tracy have?",\n  "answer": "13",\n    "explanation": "10+3=13"\n}',
    },
]

# I define a function that takes a topic string and an API key, and returns a dictionary with a quiz question, options, answer, and explanation.
def get_easy_question(api_key: str) -> Dict[str, str]:
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