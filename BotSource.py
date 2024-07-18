import os
from openai import OpenAI

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
conversation = [
    {
        "role": "system",
        "content": "You are a helpful assistant specialized in guitars. Answer all questions with a focus on guitars, guitar playing techniques, guitar maintenance, and related topics. If a question is not related to music or guitars, respond with 'I'm sorry, I can only answer questions related to guitars and music.'"
    }
] #Updated array to keep track of conversation

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