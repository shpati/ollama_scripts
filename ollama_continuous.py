import ollama

color_text = '\033[92m'
reset_text = '\033[0m'

model = 'llama3.1'
messages = []

def chat(message):
    # Add user message to history
    messages.append({'role': 'user', 'content': message})

    # Get model response with streaming
    response = ollama.chat(model=model, messages=messages, stream=True)
    
    complete_message = ''
    
    # Process the streaming response
    for chunk in response:
        content = chunk['message']['content']
        complete_message += content
        print(content, end='', flush=True)  # Print each chunk as it arrives
    
    # Append the complete assistant message to history
    messages.append({'role': 'assistant', 'content': complete_message})
    
    return complete_message

while True:
    prompt = input(f"{color_text}\n> ")
    print(f"{reset_text}")

    if (prompt.lower() == 'q') or (prompt.lower() == '/bye'):
        break
    else:
        reply = chat(prompt)
        print(f'Assistant: {reply}')