from pollinations import ask

response = ask("Tell me about Pollinations.ai.")

# Can also specify additional parameters if required, only the prompt is mandatory.
# response = ask(
#     prompt="Tell me about Polinations.ai.",
#     system_message="You are a helpful AI assistant.",
#     model="openai",
#     temperature=0.7,
#     max_tokens=800,
#     seed=239143,
#     private=False,
#     max_tries=3,
#     delays=[5,10]
# )

# If there is a problem getting the response, it will return None, so you can gracefully deal with a failed request like so:
if response is not None:
    print(f"Response from Pollinations.ai: {response}")
else:
    print("Failed to get a response from Pollinations.ai.")