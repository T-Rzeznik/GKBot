import os
from openai import OpenAI

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    organization='org-RCXMfWloXmAr0B6q9cideLet',
    project='proj_rbyAMmXk7nEiONsg85H969aH',
)


def get_gpt_response(user_input):
    message = {
        "role": "user",
        "content": user_input
    }
    response = client.chat.completions.create(
        messages = [message],
        model = "gpt-3.5-turbo",
    )
    return response.choices[0].message.content

def chat():
    while True:
        user_input = input("You: ")
        if user_input == 'exit':
          print("bye")
          break
        response = get_gpt_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chat()