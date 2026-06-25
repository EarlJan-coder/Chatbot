import requests

messages = []

while True:
    prompt = input("You: ")
    
    messages.append({
        "role": "user",
        "content" : prompt
    })
    
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model" : "qwen2.5-coder:3b",
            "messages" : messages,
            "stream" : False
        }
    )
    
    ai = response.json()['message']['content']
    print("AI:", ai)
    
    messages.append({
        "role": "assistant",
        "content" : ai
    })