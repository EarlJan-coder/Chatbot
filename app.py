from chatbot.chatbot import ChatBot
from chatbot import config

def main():
    bot = ChatBot(
        ollama_url=config.OLLAMA_URL,
        model=config.MODEL,
        timeout=config.TIMEOUT,
        save_file=config.SAVE_FILE,
    )
    bot.chat()
    
if __name__ == "__main__":
    main()