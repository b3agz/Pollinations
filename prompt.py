
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
print("Welcome to b3agz' Pollinations AI Script. Type 'exit' or 'quit' to end the program.\n\n")

prompt = input("Prompt: ")
    
try:
    print(colour_text(f"Response: {llm.get_response(prompt)}", "33"))
except PollinationsError as e:
    print(colour_text(e, "31"))

print("\n")
