
# This script should just run and work with the Pollinations.ai API (as long as it is running).
# Run it ("python ai.py" or "py ai.py", etc) and you can talk to the AI. To use it in another script,
# put this in the same folder and stick "from pollinations import ask" at the top, then just call ask("your prompt")
# from your code and store the response in a string. If it returns None, something went wrong getting a response.

import requests
import time
import random
import argparse
import os

# --------- Pollinations.ai API Data ---------
POLLINATIONS_API_URL = "https://text.pollinations.ai/openai"        # The API URL for Pollinations
POLLINATIONS_MODELS = "https://text.pollinations.ai/models"         # The API URL for listing models
POLLINATIONS_API_KEY = ""                                           # Your API key (optional, you can get one for free at https://auth.pollinations.ai/)

def ask(
    prompt,                                                         # The prompt for the AI model.
    system_message="You are a helpful AI assistant.",               # System message to set the context for the AI (optional)
    model="openai",                                                 # The model you want to use, Pollinations has a fuckton (optional, defaults to openai/GPT4.1 Nano)
    temperature=0.7,                                                # Temperature for randomness in the response, 0 = not random, 1 = most random. (optional, defaults to 1)    
    max_tokens=800,                                                 # Maximum number of tokens in the response. I think Pollinations max is 4096 (optional, defaults to 1600)
    seed=None,                                                      # Use a seed to get reproducable results. (optional, defaults to a random integer)
    private=False,                                                  # If you want the response to show in Pollinations public feed (optional, defaults to False)
    max_tries=3,                                                    # Number of times it will try to get a response before assuming something is wrong. (optional, defaults to 3)
    delays=[5, 10]                                                  # Time it waits between retries. (optional, defaults to [5, 10]
):
    """
    Send a prompt to the Pollinations API and return the response text.
    """

    # If no seed is provided, make a random one. Giving the AI the same seed will mean that, if you give
    # it the same prompt, it will return the same response. A random seed means you get a different response.
    if seed is None:
        seed = random.randint(0, 2**31 - 1)

    # Package up the data to send to Pollinations.
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "seed": seed,
        "private": private
    }

    # Set up the headers, including the API key if one was set.
    headers = {
        "Content-Type": "application/json"
    }
    if POLLINATIONS_API_KEY != "":  # Only add if it exists
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"

    # Pollinations is rate limited, especially for non-tier users (maximum of 1 request every 5 seconds).
    # This bit is in case you fire off prompts too quickly, instead of just failing, it will wait a bit and try again.
    tries = 0
    while tries < max_tries:
        
        # Try to send the request to Pollinations.
        try:
            resp = requests.post(POLLINATIONS_API_URL, json=data, headers=headers, timeout=120)
            resp.raise_for_status()
            response = resp.json()
            content = None

            # Process the response and put it into content.
            if "choices" in response and len(response["choices"]) > 0:
                msg = response["choices"][0].get("message", {})
                content = msg.get("content", None)

            # If the response does not contain content, return None. Let the function caller handle this how they want.
            if not content:
                return None
            
            # If we have valid content, strip any trailing whitespace and return it.
            return content.strip()
        
        # If the request fails, wait a bit and try again, up to max_tries times.
        except Exception as e:
            tries += 1
            if tries < max_tries:
                wait = delays[min(tries-1, len(delays)-1)]
                print(f"[Pollinations AI] Error: {e}\nRetrying in {wait} seconds... (Attempt {tries+1}/{max_tries})")
                time.sleep(wait)
            else:
                print(f"[Pollinations AI] Failed after {max_tries} attempts.\nError was: {e}")
                return None
            
def list():
    """
    Lists all of the available text models from the Pollinations API. Only the ones listed as "anonymous" can be
    accessed without an API key (free). Most of the code here is just for formatting the output.
    """
    try:
        resp = requests.get(POLLINATIONS_MODELS)
        resp.raise_for_status()
        models = resp.json()
    except Exception as e:
        print("Failed to fetch models:", e)
        return

    print("{:<20} | {:<30} | {:<20} | {:<10} | {:<10}".format("Name", "Description", "Provider", "Tier", "Vision"))
    print("-" * 90)
    for m in models:
        print("{:<20} | {:<30} | {:<20} | {:<10} | {:<10}".format(
            m.get("name", ""),
            m.get("description", "")[:27] + ("..." if len(m.get("description", "")) > 27 else ""),
            m.get("provider", ""),
            m.get("tier", ""),
            str(m.get("vision", False))
        ))

def colour_text(text, colour_code):
    """
    Makes the text a certain colour in the terminal.
    """
    return f"\033[{colour_code}m{text}\033[0m"


if __name__ == "__main__":

    # Set up the command line arguments for the script.
    parser = argparse.ArgumentParser(
        description="A script for interacting with Pollinations LLMs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--list", action="store_true", help="List available models.")
    parser.add_argument("--system-message", type=str, metavar="MSG", default="", help="Optional system message for the AI model.")
    parser.add_argument("--model", type=str, metavar="MODEL", default="openai", help="Model to use (use --list to see all models).")
    parser.add_argument("--temperature", type=float, metavar="N", default=1, help="Temperature for randomness.")
    parser.add_argument("--max-tokens", type=int, metavar="N", default=1600, help="Max tokens in the response.")
    parser.add_argument("--seed", type=int, metavar="N", default=None, help="Random seed for reproducibility.")
    parser.add_argument("--private", type=bool, metavar="N", default=False, help="Hide response from the public feed.")
    parser.add_argument("--max-tries", type=int, metavar="N", default=3, help="Max tries before failing.")
    parser.add_argument("--delays", nargs="+", type=int, metavar="SECONDS", default=[5, 10], help="Delays (in seconds) between retries.")
    args = parser.parse_args()

    # Clear the terminal and print a welcome message.
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to b3agz' Pollinations AI script. Type 'exit' or 'quit' to exit.")
    print("Be aware that this script does not handle memory, each prompt is new to the AI, it will not remember the last message.\n\n")

    # If the users wants a list of models, do that. Otherwise, enter the prompt loop.
    if args.list:
        list()
    else:
        # Loop indefinitely until the user types 'exit', 'quit' or ends the script some other way.
        while True:
            prompt = input("Prompt: ")
            if (prompt.lower() == "exit" or prompt.lower() == "quit"):
                break
            response = ask(
                prompt,
                system_message=args.system_message,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                seed=args.seed,
                private=args.private,
                max_tries=args.max_tries,
                delays=args.delays
            )
            if response is not None:
                output = f"Response: {response}"
            else:
                output = "No response received."
            
            # Print the response in a different colour and add a line break for readability.
            print(colour_text(output, "94"))
            print("\n")
        
        print("\nExiting Pollinations AI script. Goodbye!\n")