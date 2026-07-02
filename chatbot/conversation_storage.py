import json
import os
from .message import Message

class ConversationStorage:
    def __init__(self, save_file: str):
        self.save_file = save_file
    
    def load_conversation(self) -> list[Message]:
        if os.path.exists(self.save_file):
             with open(self.save_file, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):
                        return [self._message_from_data(item) for item in data]
                except (json.JSONDecodeError, ValueError):
                    print(f"Could not parse JSON form {self.save_file}")
        
        return [
            Message(role="system", content="You are a helpful Medical Assistant, you must only answer questions related to Health and Medical")
        ]

    def save_conversation(self, messages: list[Message]) -> None:
        payload = [self._message_to_dict(message) for message in messages]
        with open(self.save_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
            
    @staticmethod
    def _message_to_dict(message: Message) -> dict:
        return {"role": message.role, "content": message.content}
    
    @staticmethod
    def _message_from_data(data:object) -> Message:
        if isinstance(data, Message):
            return data
        if isinstance(data, dict):
            return Message(role=data["role"], content=data["content"])
        raise TypeError(f"Unsupported message data: {type(data)}")