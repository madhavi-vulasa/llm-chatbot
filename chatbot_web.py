from flask import Flask, request, render_template_string
import openai
from dotenv import load_dotenv
import os

# Load your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ChatGPT-like LLM Chatbot</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1470&q=80') no-repeat center center fixed;
            background-size: cover;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        h2 {
            margin-top: 30px;
            color: #fff;
            text-shadow: 2px 2px 4px #000;
        }
        form {
            margin-top: 20px;
            display: flex;
            width: 60%;
            max-width: 800px;
        }
        input[type=text] {
            flex: 1;
            padding: 12px;
            border-radius: 25px;
            border: 1px solid #ccc;
            outline: none;
        }
        input[type=submit] {
            margin-left: 10px;
            padding: 12px 20px;
            border: none;
            background-color: #4CAF50;
            color: white;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
        }
        input[type=submit]:hover {
            background-color: #45a049;
        }
        .chatbox {
            margin-top: 30px;
            width: 60%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            overflow-y: auto;
            max-height: 500px;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 20px;
            border-radius: 20px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user {
            align-self: flex-end;
            background-color: #DCF8C6;
            color: #000;
        }
        .bot {
            align-self: flex-start;
            background-color: #FFF;
            color: #000;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <h2>Chat with ChatGPT-like Bot</h2>
    <form method="post">
        <input type="text" name="message" placeholder="Type your message..." required>
        <input type="submit" value="Send">
    </form>
    <div class="chatbox">
        {% for entry in chat_history %}
            <div class="message user"><b>You:</b> {{ entry.user }}</div>
            <div class="message bot"><b>Bot:</b> {{ entry.bot }}</div>
        {% endfor %}
    </div>
</body>
</html>
"""

# Store conversation in memory (server session)
chat_history = []

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form["message"]

        # Build conversation context
        messages = [
            {"role": "system", "content": "You are ChatGPT, a helpful, creative, and concise assistant."}
        ]
        for entry in chat_history:
            messages.append({"role": "user", "content": entry["user"]})
            messages.append({"role": "assistant", "content": entry["bot"]})

        messages.append({"role": "user", "content": user_message})

        # Call OpenAI API (new style)
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )

        bot_message = response.choices[0].message.content

        # Save to history
        chat_history.append({"user": user_message, "bot": bot_message})

    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


