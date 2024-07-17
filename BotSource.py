import os
from openai import OpenAI

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
conversation = [] #Updated array to keep track of conversation

def get_gpt_response(user_input):
    message = {
        "role": "user",
        "content": user_input
    }
    conversation.append(message)
    response = client.chat.completions.create(
        messages = conversation,
        model = "gpt-3.5-turbo",
    )
    conversation.append(response.choices[0].message)
    return response.choices[0].message.content
