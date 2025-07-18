from pollinations import *

def main():

    # Initialise a Pollinations instance. Every parameters can be set on initialisation.
    llm1 = Pollinations(
        api_key = "",
        model = "openai",
        system_message = "You are a helpful AI assistant.",
        temperature = 0.7,
        top_p = 0.9,
        presence_penalty = 0.0,
        frequency_penalty = 0.0,
        as_json = False,
        max_tokens = 800,
        seed = None,
        private = False,
        timeout = 30
    )

    # Errors will raise an exception, so it's best to use try and handle exceptions gracefully.
    try:
        response = llm1.get_response("Hello, future robot overlord, how are you today?")
    except PollinationsError as e:
        response = e
    
    print(response)

    # Model parameters are optional, you can initialise with them to use defaults.
    llm2 = Pollinations()

    # But you can still set them after initialisation with the appropriate functions.
    llm2.set_model("openai-fast")
    llm2.set_temperature(1.0)

    try:
        response = llm2.get_response("Tell me a story about cats.")
    except PollinationsError as e:
        response = e

    print(response)

    # These two instances are separate, and maintain their own parameters, so you can set up specific Pollinations
    # instances and switch between them in your scripts.

if __name__ == "__main__":
    main()