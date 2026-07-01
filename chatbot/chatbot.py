from . import config
from .conversation import Conversation
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
        conversation=None,
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
        self.conversation = conversation or Conversation(self.conversation_storage)
        
    def chat(self):
        while True:
            prompt = self.ui.get_prompt()
            if prompt.lower() in {"exit", "bye", "quit"}:
                self.ui.print_exit()
                break
            
            if prompt.lower() == "reset":
                self.conversation.reset()
                self.ui.print_message("Conversation reset.")
                continue
            
            if not prompt:
                continue
            
            self.conversation.add_user(prompt)
            
            self.ui.start_assistant_output()
            response_text = self.ollama_client.generate(
                self.conversation.history,
                stream=True,
                on_token=self.ui.on_token,
            )
            self.ui.finish_assistant_output()
            
            if response_text is not None:
                self.conversation.add_assistant(response_text)
                self.conversation.save()