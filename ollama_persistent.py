import ollama
import json
import os
from datetime import datetime

# ANSI color codes
color_text = '\033[92m'
reset_text = '\033[0m'

# Configuration
model = 'llama3.1'
history_file = 'chat_history.json'

def load_chat_history():
    """Load chat history from file if it exists"""
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Could not load chat history. Starting fresh.")
            return []
    return []

def save_chat_history(messages):
    """Save chat history to file"""
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save chat history: {str(e)}")

def chat(message, messages):
    """Handle chat interaction with Ollama"""
    # Add user message to history
    messages.append({'role': 'user', 'content': message, 'timestamp': str(datetime.now())})
    
    # Get model response with streaming
    response = ollama.chat(model=model, messages=messages, stream=True)
    
    complete_message = ''
    
    # Process the streaming response
    for chunk in response:
        content = chunk['message']['content']
        complete_message += content
        print(content, end='', flush=True)  # Print each chunk as it arrives

    # Add line break if the response doesn't end with one
    if complete_message and not complete_message.endswith('\n'):
        print()  # Add missing line break
    
    # Append the complete assistant message to history
    messages.append({
        'role': 'assistant', 
        'content': complete_message,
        'timestamp': str(datetime.now())
    })
    
    # Save after each message exchange
    save_chat_history(messages)
    
    return complete_message

def main():
    print(f"\nWelcome to Ollama Chat! Your conversation will be saved in {history_file}")
    print("Type '/bye' or 'q' to quit")
    print("Type '/clear' to start a new conversation")
    
    # Load existing messages
    messages = load_chat_history()
    
    # If there are existing messages, show the last few exchanges
    if messages:
        print("\nLast conversation:")
        for msg in messages[-4:]:  # Show last 2 exchanges (4 messages)
            role = msg['role'].capitalize()
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"{role}: {content}")
    
    while True:
        prompt = input(f"{color_text}\n> ")
        print(f"{reset_text}")
        
        if prompt.lower() in ['q', '/bye']:
            print("Goodbye!")
            break
        elif prompt.lower() == '/clear':
            messages = []
            save_chat_history(messages)
            print("Chat history cleared!")
            continue
        else:
            reply = chat(prompt, messages)

if __name__ == "__main__":
    main()