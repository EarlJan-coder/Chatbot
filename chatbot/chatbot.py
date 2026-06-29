import requests
import json
from . import storage, config

class ChatBot:
    def __init__(self, ollama_url, model, timeout, save_file=config.SAVE_FILE):
        self.ollama_url = ollama_url
        self.model = model
        self.timeout = timeout
        self.save_file = save_file
        self.messages = self.load_conversation()
        
    def load_conversation(self):
        return storage.load_conversation(self.save_file)
    
    def save_conversation(self):
        return storage.save_conversation(self.messages, self.save_file)
    
    def get_prompt(self):
        return input("You: ").strip()
    
    def append_message(self, role: str, content: str) -> None:
        self.messages.append({ "role": role, "content": content })
        
    def stream_response(self) -> str | None:
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
                    except ValueError:
                        continue
                    
                    delta = chunk.get("message", {}).get("content", "")
                    if delta:
                        print(delta, end="", flush=True)
                        full_response += delta
                        
                print()
                return full_response
            
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Server may be unresponsive.")
            return None
        except requests.exceptions.RequestException as e:
            print(f'Error: Request failed - {e}')
            return None
        except ValueError as e:
            print(f'Error: Invalid Response format - {e}')
            return None
        
    def chat(self):
        while True:
            prompt = self.get_prompt()
            if prompt.lower() in {"exit", "bye", "quit"}:
                print("Exiting Chat.")
                break
            
            if not prompt:
                continue
            
            self.append_message("user", prompt)
            response_text = self.stream_response()
            
            if response_text is not None:
                self.append_message("assistant", response_text)
                self.save_conversation()