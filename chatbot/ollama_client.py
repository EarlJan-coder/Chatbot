import requests
import json

class OllamaClient:
    def __init__(self, ollama_url: str, model: str, timeout: int):
        self.ollama_url = ollama_url
        self.model = model
        self.timeout = timeout
        
    def generate(self, messages: list[dict], stream: bool, on_token=None) -> str | None:
        try:
            with requests.post(
                self.ollama_url,
                json={
                    "model" : self.model,
                    "messages" : messages,
                    "stream" : stream,
                },
                stream=stream,
                timeout=self.timeout,
            ) as response:
                response.raise_for_status()
                
                if not stream:
                    payload = response.json()
                    return payload.get("message", {}).get("content", "")
                
                full_response = ""
                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    
                    try:
                        chunk = json.loads(line)
                    except ValueError:
                        continue
                    
                    delta = chunk.get("message", {}).get("content", "")
                    if delta:
                        if on_token is not None:
                            on_token(delta)
                        full_response += delta
                
                return full_response
                
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Server may be unresponsive.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: Request failed - {e}")
            return None
        except ValueError as e:
            print(f"Error: Invalid response format - {e}")
            return None
        