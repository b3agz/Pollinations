# pollinations.py

A simple, ready-to-use Python client for the [Pollinations.ai](https://pollinations.ai) API.

Provides a `Pollinations()` class that can be created and called at runtime using either `get_response()` (for a single prompt/response) or `chat()` (for a response with message history context). All of the paramters that Pollinations expose are settable in the initialisation and modifiable using functions like `set_temperature()`, `set_model()`, etc.

Some models are not available for anonymous use, you can get an API key at https://auth.pollinations.ai, and set it either by setting `api_key` when initalising your class or by using `set_api_key()` after initialisation. You can print a list of available models to terminal with `print_model_list()`, or just run `list.py`.

**Please note I AM NOT affiliated with Pollinations.ai, they are not responsible for this script and I am not responsible for their servers. You are responsible for your own usage, however. Pollination.ai are doing a cool thing, don't abuse it.**

---

## Features

- Run `prompt.py` to test out a single prompt.
- Run `chat.py` to test chat with message history.
- Run `list.py` to see a list of available models and details.
- `example.py` shows a basic usage example.
- All parameters exposed by Pollinations (at the time of writing) can be set.
- Internally handles message history for chat-like behaviour.
- No login or API key required for anonymous models (but can use one if you want)

### Example Usage

```bash
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
```

---

## Requirements

- Python 3.8+
- `requests` library

## Installation

Clone or download this repo, then install the requirements:

```bash
git clone https://github.com/b3agz/Pollinations.git
cd pollinations
pip install -r requirements.txt
```

## License

MIT License. See [LICENSE](LICENSE) for details.
