import os
from pollinations import *

llm = Pollinations()

# Clear the terminal and print a welcome message.
os.system('cls' if os.name == 'nt' else 'clear')
print("This script attempts to get the currently available text models from Pollinations.ai")
print("and print them to the terminal. The Name field is what you should pass in as model")
print("if you want to change from the default. The ones listed as anonymous under Tier can be")
print("used without an API key.\n\n")

try:
    llm.print_models_list()
except PollinationsError as e:
    print(e)