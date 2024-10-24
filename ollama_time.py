import datetime
import json
import requests

color_text = '\033[92m'
reset_text = '\033[0m'

model = 'llama3.1'

def get_current_datetime():
    """Get current date and time formatted as a string"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def send_prompt_to_ollama(prompt, model=model):
    """Send a prompt to Ollama and get the response"""
    url = "http://localhost:11434/api/generate"
    
    # Include current date/time in the system prompt
    current_time = get_current_datetime()
    system_prompt = f"Current date and time is: {current_time}. You can reference this in your responses."
    
    data = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {str(e)}"

def main():
    # Example usage
    while True:
        user_input = input(f"{color_text}\n> ")
        print(f"{reset_text}")
        
        if user_input.lower() in ["/bye", "bye", "exit", "quit", "close"]:
            break
            
        response = send_prompt_to_ollama(user_input)
        print("Ollama's response:")
        print(response)

if __name__ == "__main__":
    print("\nStarting Ollama chat with datetime awareness...")
    print("Make sure Ollama is running locally!")
    main()