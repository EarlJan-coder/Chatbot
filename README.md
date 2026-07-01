# Advanced Python Chatbot

A terminal-based chatbot built with Python that connects to a local Ollama model, streams responses in the CLI, and keeps conversation history between sessions.

## Current progress
- Interactive terminal chat loop
- Streaming assistant responses token by token from Ollama
- Persistent conversation history saved to a JSON file
- Conversation reset support with the reset command
- Configuration loaded from a .env file
- Modular project structure for the UI, conversation logic, storage, and Ollama client

## Setup
1. Create a .env file with:
   - OLLAMA_URL
   - MODEL
   - TIMEOUT (optional, defaults to 120)
2. Install the required packages if needed:
   - pip install requests python-dotenv
3. Start the app:
   - python app.py

## Commands
- Type exit, bye, or quit to stop the chat
- Type reset to clear the current conversation history

