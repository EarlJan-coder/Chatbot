from . import config
from .conversation_storage import ConversationStorage
from .ollama_client import OllamaClient
from .terminal_ui import TerminalUI


class ChatBot:
    def __init__(
        self,
        ollama_url,
        model,
        timeout,
        save_file=config.SAVE_FILE,
        ui=None,
        ollama_client=None,
        conversation_storage=None,
    ):
        self.ollama_url = ollama_url
        self.model = model
        self.timeout = timeout
        self.save_file = save_file
        
        self.ui = ui or TerminalUI()
        self.ollama_client = ollama_client or OllamaClient(
            ollama_url=ollama_url,
            model=model,
            timeout=timeout,
        )
        self.conversation_storage = conversation_storage or ConversationStorage(save_file)
        self.messages = self.conversation_storage.load_conversation()
        
    def append_message(self, role: str, content: str) -> None:
        self.messages.append({ "role":role, "content":content })
        
    def chat(self):
        while True:
            prompt = self.ui.get_prompt()
            if prompt.lower() in {"exit", "bye", "quit"}:
                self.ui.print_exit()
                break
            
            if not prompt:
                continue
            
            self.append_message("user", prompt)
            
            self.ui.start_assistant_output()
            response_text = self.ollama_client.generate(
                self.messages, 
                stream=True, 
                on_token=self.ui.on_token
            )
            
            self.ui.finish_assistant_output()
            
            if response_text is not None:
                self.append_message("assistant", response_text)
                self.conversation_storage.save_conversation(self.messages)