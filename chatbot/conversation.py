from .conversation_storage import ConversationStorage

DEFAULT_CONVERSATION = [
    {
        "role":"system",
        "content":"You are a helpful AI assistant"
     }
]

class Conversation():
    def __init__(self, storage: ConversationStorage):
        self.storage = storage
        self._messages = self.storage.load_conversation()
        
    @property
    def history(self) -> list[dict]:
        return self._messages
    
    def add_user(self, content: str) -> None:
        self._add_message("user", content)
        
    def add_assistant(self, content: str) -> None:
        self._add_message("assistant", content)
        
    def _add_message(self, role: str, content: str) -> None:
        self._messages.append({ "role":role, "content":content })
        
    def save(self) -> None:
        self.storage.save_conversation(self._messages)
        
    def reset(self) -> None:
        self._messages = [dict(m) for m in DEFAULT_CONVERSATION]
        self.save()