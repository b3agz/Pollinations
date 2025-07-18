
import os
from pollinations import *

llm = Pollinations()

def colour_text(text, colour_code):
    """
    Makes the text a certain colour in the terminal.
    """
    return f"\033[{colour_code}m{text}\033[0m"

# Clear the terminal and print a welcome message.
os.system('cls' if os.name == 'nt' else 'clear')
print("Welcome to b3agz' Pollinations AI Chat. Type 'exit' or 'quit' to end the program.")
print("This chat is context aware (it remembers previous messages) but only up to")
print("a guestimate of Pollinations.ai's max token length. When it gets")
print("near that length, it starts trimming off the oldest parts of the chat to")
print("remain within the token length.\n\n")

# Enter into a perpetual loop until the user ends the script.
while True:
    prompt = input("Prompt: ")
    if (prompt.lower() == "exit" or prompt.lower() == "quit"):
        break
        
    try:
        print(colour_text(f"Response: {llm.chat(prompt)}", "33"))
    except PollinationsError as e:
        print(colour_text(e, "31"))
    
    print("\n")

print("\nExiting Pollinations AI script. Goodbye!\n")