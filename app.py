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
    
    
    if not bot.ollama_url or not bot.model:
        raise ValueError("Missing key")
    
if __name__ == "__main__":
    main()