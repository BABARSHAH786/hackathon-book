
from openai import OpenAI

# Your Gemini API key
GEMINI_API_KEY = "AIzaSyDE-eLpOdx-6P1l8S78hCGd-VqHhGLX5qw"

# Configure OpenAI client to use Gemini API
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_chatbot_response(prompt: str) -> str:
    try:
        chat_completion = client.chat.completions.create(
            model="gemini-pro",  # Using gemini-pro model
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Chatbot initialized. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = get_chatbot_response(user_input)
        print(f"Chatbot: {response}")
