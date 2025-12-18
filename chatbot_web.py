from flask import Flask, request, render_template_string, redirect, url_for
import openai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LLM Chatbot</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1470&q=80') no-repeat center center fixed;
            background-size: cover;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.2);
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 90vh;
        }
        .header {
            background-color: #007BFF;
            color: white;
            padding: 15px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h2 {
            margin: 0;
            font-size: 1.5em;
        }
        .chatbox {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background-color: #f9f9f9;
        }
        .user {
            background-color: #007BFF;
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            display: inline-block;
            margin: 5px 0;
        }
        .bot {
            background-color: #e2e2e2;
            color: black;
            padding: 8px 12px;
            border-radius: 20px;
            display: inline-block;
            margin: 5px 0;
        }
        form {
            display: flex;
            padding: 15px;
            gap: 10px;
            border-top: 1px solid #ccc;
        }
        input[type=text] {
            flex: 1;
            padding: 10px;
            border-radius: 20px;
            border: 1px solid #ccc;
        }
        input[type=submit], button {
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
        }
        input[type=submit] { background-color: #28a745; color: white; }
        button { background-color: #dc3545; color: white; }
        .typing { font-style: italic; color: #555; margin: 5px 0; }
        @media screen and (max-width: 768px) {
            .container { width: 95%; height: 90vh; }
            input[type=text] { padding: 8px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>LLM Chatbot</h2>
            <form method="post" action="/clear">
                <button type="submit">Clear Chat</button>
            </form>
        </div>
        <div class="chatbox" id="chatbox">
            {% for entry in chat_history %}
                <div class="user"><b>You:</b> {{ entry.user }}</div>
                <div class="bot"><b>Bot:</b> {{ entry.bot }}</div>
            {% endfor %}
        </div>
        <form method="post" id="chatForm">
            <input type="text" name="message" placeholder="Type your message" required autofocus>
            <input type="submit" value="Send">
        </form>
        <div class="typing" id="typingIndicator" style="display:none;">Bot is typing...</div>
    </div>

    <script>
        const chatForm = document.getElementById('chatForm');
        const chatbox = document.getElementById('chatbox');
        const typingIndicator = document.getElementById('typingIndicator');

        chatForm.addEventListener('submit', function() {
            typingIndicator.style.display = 'block';
        });

        function scrollToBottom() {
            chatbox.scrollTo({ top: chatbox.scrollHeight, behavior: 'smooth' });
        }

        // Scroll to bottom on load
        scrollToBottom();
    </script>
</body>
</html>
"""

chat_history = []

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form["message"]

        messages = [
            {"role": "system", "content": "You are ChatGPT, a helpful, concise, and creative assistant."}
        ]
        for entry in chat_history:
            messages.append({"role": "user", "content": entry["user"]})
            messages.append({"role": "assistant", "content": entry["bot"]})
        messages.append({"role": "user", "content": user_message})

        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )

        bot_message = response.choices[0].message.content
        chat_history.append({"user": user_message, "bot": bot_message})

    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)

@app.route("/clear", methods=["POST"])
def clear():
    chat_history.clear()
    return redirect(url_for("chat"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

