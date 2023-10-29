# get_quiz.py
import json
from typing import Dict

import openai

# I have some chat history saved in a list, where each item is a dictionary representing a message with a role and content.
chat_history = [
    {
        "role": "system",
        "content": "You are a REST API server with an endpoint /generate-random-question, which generates unique primary school level medium difficulty math quiz question about fractions in json data.",
    },
    {"role": "user", "content": "GET /generate-random-question/devops"},
    {
        "role": "assistant",
        "content": '\n\n{\n    "question": "What is the numerator in the fraction 5/2?",\n "answer": "5",\n    "explanation": "The numerator is the number that is above the fraction size"\n}',
    },
    {"role": "user", "content": "GET /generate-random-question/jenkins"},
     {
        "role": "assistant",
        "content": '\n\n{\n    "question": "What is 1/3 * 6",\n  "answer": "2",\n    "6*1=6, 6/3=2. So the answer is 2"\n}',
    },
]

# I define a function that takes a topic string and an API key, and returns a dictionary with a quiz question, options, answer, and explanation.
def get_medium_question(api_key: str) -> Dict[str, str]:
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