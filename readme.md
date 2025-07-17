# pollinations.py

A simple, ready-to-use Python client for the [Pollinations.ai](https://pollinations.ai) API.

Talk to LLMs with a command-line interface, or use the `ask()` function directly in your own scripts. Can be used with with just a prompt and the default settings or you can set your own settings as needed (see below).

Some models are not available for anonymous use, you can get an API key at https://auth.pollinations.ai, just set `POLLINATIONS_API_KEY` to that key and you should be able to access
models on the appropriate tier.

**Please note I AM NOT affiliated with Pollinations.ai, they are not responsible for this script and I am not responsible for their servers. You are responsible for your own usage, however. Pollination.ai are doing a cool thing, don't abuse it.**

---

## Features

- Query Pollinations LLMs interactively from the terminal
- Call the `ask()` function from your own Python projects
- List all available models (and see which ones are free/anonymous)
- Set system prompts (“context”) for the model
- Optional parameters for reproducibility, randomness, model, and more
- Handles retries and rate limits automatically
- No login or API key required for anonymous models (but can use one if you want)

### CLI Options

```bash
usage: pollinations.py [-h] [--list] [--system-message MSG] [--model MODEL]
                       [--temperature N] [--max-tokens N] [--seed N]
                       [--private N] [--max-tries N] [--delays SECONDS [SECONDS ...]]

A script for interacting with Pollinations LLMs.

optional arguments:
  -h, --help            show this help message and exit
  --list                List available models. (default: False)
  --system-message MSG  Optional system message for the AI model. (default: )
  --model MODEL         Model to use (use --list to see all models). (default: openai)
  --temperature N       Temperature for randomness. (default: 1)
  --max-tokens N        Max tokens in the response. (default: 1600)
  --seed N              Random seed for reproducibility. (default: None)
  --private N           Hide response from the public feed. (default: False)
  --max-tries N         Max tries before failing. (default: 3)
  --delays SECONDS [SECONDS ...]
                        Delays (in seconds) between retries. (default: [5, 10])
```

---

## Requirements

- Python 3.8+
- `requests` library

## Installation

Clone or download this repo, then install the requirements:

```bash
git clone https://github.com/b3agz/Pollinations.git
cd pollinations.py
pip install -r requirements.txt
```

## License

MIT License. See [LICENSE](LICENSE) for details.
