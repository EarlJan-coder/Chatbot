import json
import requests

messages = []

while True:
    prompt = input("You: ").strip()
    
    if prompt.lower() in ["exit", "quit", "bye"]:
        print("Exiting chat.")
        break
    
    if not prompt:
        continue
    
    messages.append({
        "role": "user",
        "content" : prompt
    })
    
    try:
        with requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model" : "qwen2.5-coder:3b",
                "messages" : messages,
                "stream" : True
            },
            stream=True,
            timeout=30
        ) as response:
            response.raise_for_status()
            
            full_response = ""
            print("AI:", end=" ", flush=True)
            
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                delta = chunk.get("message", {}).get("content", "")
                if delta:
                    print(delta, end="", flush=True)
                    full_response += delta
                    
            print()
            
        messages.append({
            "role" : "assistant",
            "content" : full_response
        })
    
    except requests.exceptions.Timeout:
        print("Error: Request Timed out. Server may be unresponsive.")
        messages.pop()
        
    except requests.exceptions.RequestException as e:
        print(f'Error: Request failed - {e}')
        messages.pop()
        
    except(KeyError, ValueError, json.JSONDecodeError) as e:
        print(f'Error: Invalid response format - {e}')
        messages.pop()