import requests

messages = []

while True:
    prompt = input("You: ")
    
    messages.append({
        "role": "user",
        "content" : prompt
    })
    
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model" : "qwen2.5-coder:3b",
                "messages" : messages,
                "stream" : False
            },
            timeout=30
        )
        response.raise_for_status()
        ai = response.json()['message']['content']
        print("AI:", ai)
        
        messages.append({
            "role": "assistant",
            "content" : ai
        })
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Server may be unresponsive.")
        messages.pop()
        continue
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed - {e}")
        messages.pop()
        continue
    except (KeyError, ValueError) as e:
        print(f"Error: Invalid response format - {e}")
        messages.pop()
        continue