import json
import os

class ConversationStorage:
    def __init__(self, save_file: str):
        self.save_file = save_file
    
    def load_conversation(self) -> list[dict]:
        if os.path.exists(self.save_file):
             with open(self.save_file, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):
                        return data
                except (json.JSONDecodeError, ValueError):
                    print(f"Could not parse JSON form {self.save_file}")
        
        return [
            {
                "role" : "system",
                "content" : "You are a helpful AI assistant"
            }
        ]

    def save_conversation(self, messages: list[dict]) -> None:
        with open(self.save_file, "w", encoding="utf-8") as file:
            json.dump(messages, file, indent=2)