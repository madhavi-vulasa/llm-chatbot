from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)  # Check if Python sees your key
if not api_key:
    raise ValueError("OpenAI API key not found. Check your .env file.")
# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Conversation memory
conversation = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("Chatbot started. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Exiting chatbot. Goodbye!")
        break

    # Add user message to conversation
    conversation.append({"role": "user", "content": user_input})

    # Get response from the LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        temperature=0.7
    )

    # Extract assistant reply
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})

    print("Bot:", reply, "\n")

