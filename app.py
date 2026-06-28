import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")
TIMEOUT = float(os.getenv("TIMEOUT", 120))
SAVE_FILE = os.path.join(os.path.dirname(__file__), "conversation.json")


class ChatBot:
    def __init__(self, ollama_url, model, timeout, save_file=SAVE_FILE):
        self.ollama_url = ollama_url
        self.model = model
        self.timeout = timeout
        self.save_file = save_file
        self.messages = self.load_conversation()
        
    def load_conversation(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                
        return [
            {
                "role" : "system",
                "content" : "You are a helpful Python AI assistant"
            }
        ]
        
    def save_conversation(self):
        with open(self.save_file, "w", encoding="utf-8") as file:
            json.dump(self.messages, file, indent=2)
        
    def get_prompt(self):
        return input("You: ").strip()
    
    def append_message(self, role, content):
        self.messages.append({
            "role" : role,
            "content" : content
        })
        self.save_conversation()
        
    def stream_response(self):
        try:
            with requests.post(
                self.ollama_url,
                json={
                    "model" : self.model,
                    "messages" : self.messages,
                    "stream" : True
                },
                stream=True,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                
                full_response = ""
                print("AI:", end=" ", flush=True)
                
                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    
                    delta = chunk.get("message", {}).get("content", "")
                    if delta:
                        print(delta, end="", flush=True)
                        full_response += delta
                
                print()
        except requests.exceptions.Timeout:
            print("Error: Request Timed out. Server may be unresponsive.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: Request failed - {e}")
            return None

        except (KeyError, ValueError, json.JSONDecodeError) as e:
            print(f"Error: Invalid response format - {e}")
            return None
    
    def chat(self):
        while True:
            prompt = self.get_prompt()
            
            if prompt.lower() in ['exit', 'bye', 'quit']:
                print("Exiting chat...")
                break
                
            if not prompt:
                continue
            
            self.append_message("user", prompt)
            
            response_text = self.stream_response()
            if response_text is not None:
                self.append_message("assistant", response_text)

def main():
    bot = ChatBot(OLLAMA_URL, MODEL, TIMEOUT)
    bot.chat()
    

if __name__ == "__main__":
    main()
        