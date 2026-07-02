from .conversation_storage import ConversationStorage
from .message import Message

DEFAULT_CONVERSATION = [
    Message(role="system", content="You are a helpful Medical Assistant, you must only answer questions related to Health and Medical")
]

class Conversation():
    def __init__(self, storage: ConversationStorage):
        self.storage = storage
        self._messages : list[Message] = self.storage.load_conversation()
        
    @property
    def history(self) -> list[Message]:
        return self._messages
    
    def add_user(self, content: str) -> None:
        self._add_message("user", content)
        
    def add_assistant(self, content: str) -> None:
        self._add_message("assistant", content)
        
    def _add_message(self, role: str, content: str) -> None:
        self._messages.append(Message(role=role, content=content))
        
    def save(self) -> None:
        self.storage.save_conversation(self._messages)
        
    def reset(self) -> None:
        self._messages = [Message(role=m.role, content=m.content) for m in DEFAULT_CONVERSATION]
        self.save()