class TerminalUI:
    def get_prompt(self) -> str:
        return input("You: ").strip()
    
    def start_assistant_output(self):
        print("AI:", end="", flush=True)
            
    def on_token(self, delta: str):
        print(delta, end="", flush=True)
        
    def finish_assistant_output(self):
        print()    
            
    def print_error(self, message: str) -> None:
        print(message)
        
    def print_exit(self) -> None:
        print("Exiting")