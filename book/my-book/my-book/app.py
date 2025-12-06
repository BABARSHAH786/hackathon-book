from flask import Flask, request, jsonify, send_from_directory
from chatbot import get_chatbot_response
import os

app = Flask(__name__)

# Serve the index.html file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# API endpoint for chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    chatbot_response = get_chatbot_response(user_message)
    return jsonify({'response': chatbot_response})

if __name__ == '__main__':
    # Ensure chatbot.py is in the same directory
    if not os.path.exists('chatbot.py'):
        print("Error: chatbot.py not found in the current directory.")
        exit(1)

    app.run(debug=True)
