import requests

chat = input("Enter Prompt: ")

try:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen2.5-coder:3b",
            "messages": [
                {
                    "role" : "user",
                    "content" : chat
                }
            ],
            "stream": False
        },
        timeout=60
    )
    
    response.raise_for_status()
    
    data = response.json()
    print("\nAI: ", data['message']['content'])

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")