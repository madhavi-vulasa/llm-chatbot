from flask import Flask, request, render_template_string
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# HTML template for the chat page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LLM Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input[type=text] { width: 80%; padding: 10px; }
        input[type=submit] { padding: 10px; }
        .chatbox { margin-top: 20px; }
        .user { color: blue; }
        .bot { color: green; }
    </style>
</head>
<body>
    <h2>Chat with LLM Chatbot</h2>
    <form method="post">
        <input type="text" name="message" placeholder="Type your message" required>
        <input type="submit" value="Send">
    </form>
    <div class="chatbox">
        {% for entry in chat_history %}
            <p class="user"><b>You:</b> {{ entry.user }}</p>
            <p class="bot"><b>Bot:</b> {{ entry.bot }}</p>
        {% endfor %}
    </div>
</body>
</html>
"""

# Store chat history in memory (resets on server restart)
chat_history = []

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form["message"]

        # Call OpenAI API using the new interface
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Access bot response correctly
        bot_message = response.choices[0].message.content
        chat_history.append({"user": user_message, "bot": bot_message})

    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
