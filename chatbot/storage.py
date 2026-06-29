import json
import os

def load_conversation(save_file):
        if os.path.exists(save_file):
            with open(save_file, "r", encoding="utf-8") as file:
                try: 
                    data = json.load(file)
    
                    if not isinstance(data, list):
                        return []
                    
                except (json.JSONDecodeError, ValueError):
                    print(f"Could not parse JSON from {save_file}")
                    return []
                    
        return [
            {
                "role" : "system",
                "content" : "You are a helpful Python AI assistant"
            }
        ]
        
def save_conversation(messages, save_file):
    with open(save_file, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=2)