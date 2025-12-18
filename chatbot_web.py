from flask import Flask, request, render_template_string
import openai
from dotenv import load_dotenv
import os

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
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1470&q=80') no-repeat center center fixed;
            background-size: cover;
        }
        header {
            background-color: rgba(0,0,0,0.6);
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 24px;
        }
        form {
            margin: 20px;
            display: flex;
            justify-content: center;
        }
        input[type=text] {
            width: 70%;
            padding: 10px;
            border-radius: 5px;
            border: none;
        }
        input[type=submit], button {
            padding: 10px 15px;
            margin-left: 10px;
            border-radius: 5px;
            border: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }
        .chatbox {
            margin: 20px auto;
            width: 80%;
            max-width: 800px;
            background-color: rgba(255,255,255,0.85);
            padding: 20px;
            border-radius: 10px;
            height: 500px;
            overflow-y: auto;
        }
        .message {
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #d0ebff; /* light blue */
            text-align: left;
            margin-left: 0;
        }
        .bot-message {
            background-color: #d3f9d8; /* light green */
            text-align: left;
            margin-left: 20px; /* indent bot messages */
        }
    </style>
    <script>
        function clearChat() {
            fetch('/clear', {method: 'POST'}).then(() => { location.reload(); });
        }
        window.onload = function() {
            var chatbox = document.querySelector('.chatbox');
            chatbox.scrollTop = chatbox.scrollHeight; // scroll to bottom
        };
    </script>
</head>
<body>
    <header>🌿 LLM Chatbot</header>
    <form method="post">
        <input type="text" name="message" placeholder="Type your message" required>
        <input type="submit" value="Send">
        <button type="button" onclick="clearChat()">Clear Chat</button>
    </form>
    <div class="chatbox">
        {% for entry in chat_history %}
            <div class="message user-message">
                <b>You:</b> {{ entry.user }}
            </div>
            <div class="message bot-message">
                <b>Bot:</b> {{ entry.bot }}
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

chat_history = []

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form.get("message", "").strip()
        if user_message:  # only process non-empty messages
            # build messages for OpenAI
            messages = [{"role": "system", "content": "You are ChatGPT, a helpful assistant."}]
            for entry in chat_history:
                messages.append({"role": "user", "content": entry["user"]})
                messages.append({"role": "assistant", "content": entry["bot"]})
            messages.append({"role": "user", "content": user_message})

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            bot_message = response.choices[0].message.content
            chat_history.append({"user": user_message, "bot": bot_message})

        return redirect(url_for("chat"))  # redirect after POST to prevent resubmission

    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)


@app.route("/clear", methods=["POST"])
def clear():
    global chat_history
    chat_history = []
    return ("", 204)  # No Content for smooth JS reload

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
