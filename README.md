# Advanced Python Chatbot

A simple terminal-based chatbot built with Python that connects to an Ollama model, streams responses in the CLI, and saves conversation history to a JSON file.

## Current progress
- Interactive chat loop in the terminal
- Streaming AI responses from Ollama
- Persistent conversation storage in conversation.json
- Basic configuration through environment variables

## Run it
1. Create a .env file with:
   - OLLAMA_URL
   - MODEL
   - TIMEOUT (optional)
2. Start the app:
   - python app.py

Type exit, bye, or quit to stop the chat.
