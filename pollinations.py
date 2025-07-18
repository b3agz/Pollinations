__all__ = ["Pollinations", "PollinationsError"]

import random
import requests
from typing import Optional, List, Dict, Any

class PollinationsError(Exception):
    """Base exception for all Pollinations client errors."""
    pass

class Pollinations:

    """
    Class for interfacing with the Pollinations.ai API. Initialise with desired values.
    Values can be changed after initialisation using set functions (eg set_api_key(), set_model(), etc).

    Args:
        api_key: Your Pollinations.ai API key (obtained at https://auth.pollinations.ai). Not required for use but some models are only available with an API key. (Optional)
        model: The LLM model to use. Use Pollinations.list_models() to get available models. (Optional, defaults to "openai")
        system_message: The system prompt given to the AI, often used to tell it the purpose it is serving. (Optional, defaults to "You are a helpful AI assistant.")
        temperature: 0.0 - 1.0 inclusive, determines how "creative" the model is. A higher number is more creative but more prone to hallucination. (Optional, defaults to 0.7)
        top_p: 0.0 - 1.0 inclusive, similar to temperature, higher value = more creative. (Optional, defaults to 0.9)
        presence_penalty: -2.0 to 2.0 inclusive, higher values encouraging less topic repetition. (Optional, defaults to 0.0)
        frequency_penalty: -2.0 to 2.0 inclusive, higher values reduce repitition at the word/phrase level. (Optional, defaults to 0.0)
        as_json: If True, tells the LLM to respond in JSON format. (Optional, defaults to False)
        max_tokens: The maximum number of tokens the LLM will process. Automatically clamped between 0 and Pollinations.POLLINATIONS_MAX_TOKENS (Optional, defaults to 800)
        seed: Using a seed ensures repeatable results. Class seed can be overridden when sending a request to the model. If left as None, a random seed is used. (Optional, defaults to None)
        private: If True, responses will NOT show up in the public Pollinations.ai feed. (Optional, defaults to False)
        timeout: How long we wait for the LLM to respond before assuming there's a problem and throwing an exception.
    """

    def __init__(
            self,
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
            ):

        # Set parameters using the set functions for validation.
        self.set_api_key(api_key)
        self.set_model(model)
        self.set_system_message(system_message)
        self.set_temperature(temperature)
        self.set_top_p(top_p)
        self.set_presence_penalty(presence_penalty)
        self.set_frequency_penalty(frequency_penalty)
        self.set_json(as_json)
        self.set_max_tokens(max_tokens)
        self.set_seed(seed)
        self.set_private(private)
        self.set_timeout(timeout)

        self.chat_history = [
            {"role": "system", "content": system_message}
        ]

# --------- Pollinations.ai API Data ---------

    POLLINATIONS_API_URL = "https://text.pollinations.ai/openai"        # The API URL for Pollinations
    POLLINATIONS_MODELS_URL = "https://text.pollinations.ai/models"     # The API URL for listing models
    POLLINATIONS_MAX_TOKENS = 4096                                      # Maximum number of tokens Pollinations allows (I think)

# --------- Functions for setting the AI's parameters ---------

    def set_api_key(self, api_key: str):
        """ Sets the API Key (can be empty). """
        if not isinstance(api_key, str):
            raise PollinationsError("API Key must be a string.")
        self.api_key = api_key
        
    def set_system_message(self, system_message: str):
        """ Sets the AI's system message (can be empty) """
        if not isinstance(system_message, str):
            raise PollinationsError("System Message must be string, eg; \"You are a helful AI assistant\".")
        self.system_message = system_message

    def set_model(self, model: str):
        """ Sets the AI's model, use list_models() to see available models. """
        if not isinstance(model, str) or model == "":
            raise PollinationsError("Model must be a string. eg; \"openai-large\", and cannot be empty.")
        self.model = model

    def set_temperature(self, temperature):
        """ Sets the model temperature (0-1) """
        if not isinstance(temperature, (float, int)) or not (0 <= float(temperature) <= 1):
            raise PollinationsError("Temperature must be a float between 0 and 1 (inclusive)")
        # Cast to float in case an int (0 or 1) was passed in.
        self.temperature = float(temperature)

    def set_presence_penalty(self, presence_penalty):
        """ Sets the presence penalty value, automatically clamps between -2.0 and 2.0 """
        if not isinstance(presence_penalty, (float, int)):
            raise PollinationsError("Presence Penalty must be a float or an int.")
        self.presence_penalty = max(-2.0, min(float(presence_penalty), 2.0))
    
    def set_frequency_penalty(self, frequency_penalty):
        """ Sets the frequency penalty value, automatically clamps between -2.0 and 2.0 """
        if not isinstance(frequency_penalty, (float, int)):
            raise PollinationsError("Frequency Penalty must be a float or an int.")
        self.frequency_penalty = max(-2.0, min(float(frequency_penalty), 2.0))

    def set_top_p(self, top_p):
        """ Sets the top_p value, automatically clamps between 0.0 and 1.0 """
        if not isinstance(top_p, (float, int)):
            raise PollinationsError("top_p must be a float or an int.")
        self.top_p = max(0.0, min(float(top_p), 1.0))

    def set_json(self, json: bool):
        """ Set whether the model should respond in JSON format or not. """
        if not isinstance(json, bool):
            raise PollinationsError("JSON must be a bool.")
        self.as_json = json

    def set_max_tokens(self, max_tokens: int):
        """ Sets the model's max tokens, automatically clamped between 0 and POLLINATIONS_MAX_TOKENS """
        if not isinstance(max_tokens, int):
            raise PollinationsError("Max Tokens must be an int.")
        self.max_tokens = max(0, min(max_tokens, type(self).POLLINATIONS_MAX_TOKENS))

    def set_seed(self, seed):
        """ Sets the model's seed, can be left as None. """
        if seed is not None and not isinstance(seed, int):
            raise PollinationsError("Seed must be an int.")
        self.seed = seed

    def set_private(self, private: bool):
        """ Set whether responses show up in Pollinations.ai's public feed (False = NOT private and WILL show in the feed). """
        if not isinstance(private, bool):
            raise PollinationsError("Private must be a bool.")
        self.private = private

    def set_timeout(self, timeout):
        """ Sets how long we wait for a response before throwing an exception. """
        if timeout is not None and not isinstance(timeout, (int, float)):
            raise PollinationsError("Timeout must be an int or a float.")
        self.timeout = float(timeout)

    def _count_message_tokens(self, message: dict) -> int:
        # Basic word count approximation (you can replace with tiktoken if available)
        return len(message['content'].split())

    def _trim_history_to_fit(self, max_tokens: int, reserved_response_tokens: int = 100) -> list:
        """
        Trims the message history so the total tokens fit within max_tokens.
        - Always keeps the system message and the most recent exchanges.
        - reserved_response_tokens: Number of tokens to leave for the model's reply.
        """
        history = self.chat_history.copy()
        total_tokens = sum(self._count_message_tokens(m) for m in history)
        
        # While over budget (minus space for the response), trim oldest non-system message
        while len(history) > 2 and (total_tokens + reserved_response_tokens) > max_tokens:
            # Remove second message (preserve system message at start)
            removed = history.pop(1)
            total_tokens -= self._count_message_tokens(removed)

        return history

    def get_response(
            self,
            prompt: Optional[str] = None,
            messages: Optional[List[Dict[str, str]]] = None,
            seed: Optional[int] = None
            ) -> str:

        """
        Sends a prompt to the Pollinations API and returns the response.

        Args:
            prompt: A single user prompt. If provided, used as the user message with system prompt.
            messages: A full chat history, as a list of {"role": ..., "content": ...} dicts.
            seed: Using a seed ensures a repeatable response. If not set, will use the class seed. If class seed is not set, will use a random seed.

        Returns:
            The AI response as a string or raises an exception on failure.
        """

        # Determine which message structure to use
        if messages is not None:
            msg_list = messages
        elif prompt is not None:
            msg_list = [
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt}
            ]
        else:
            raise PollinationsError("You must provide either a prompt or a messages list.")

        # If seed was passed, use that, otherwise use the class instance seed.
        seed = seed if seed is not None else self.seed

        # If seed is still None, generate a random seed and use that.
        if seed is None:
            seed = random.randint(0, 2**31 - 1)

        # Package up the data to send to Pollinations.
        data = {
            "model": self.model,
            "messages": msg_list,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "json": self.as_json,
            "max_tokens": self.max_tokens,
            "seed": seed,
            "private": self.private
        }

        # Set up the headers, including the API key if one has been set.
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key != "":
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Try to send the request to Pollinations.
        try:
            resp = requests.post(type(self).POLLINATIONS_API_URL, json=data, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            response = resp.json()
            content = None

            # Handle unexpected responses better
            if "choices" in response and len(response["choices"]) > 0:
                msg = response["choices"][0].get("message", {})
                content = msg.get("content", None)

            if not content:
                # Show more of the API response for debugging
                raise PollinationsError(f"No content in Pollinations response. Raw response: {response}")

            return content.strip()

        except Exception as e:
            raise PollinationsError(f"Pollinations request failed: {e}")
        
    def chat(self, message: str) -> str:
        # Add user message to chat history
        self.chat_history.append({"role": "user", "content": message})

        # Trim history to fit within token limits before sending
        trimmed_history = self._trim_history_to_fit(self.POLLINATIONS_MAX_TOKENS)

        # Get response using trimmed history
        reply = self.get_response(messages=trimmed_history)

        # Add assistant's reply to *full* history (so user can see entire conversation if desired)
        self.chat_history.append({"role": "assistant", "content": reply})

        return reply

    def list_models(self) -> List[Dict[str, Any]]:
        """
        Fetches and returns the available text models from the Pollinations API.

        Returns:
            List of dictionaries, each containing model information (e.g., name, description, provider, tier, vision).

        Raises:
            PollinationsError: if there is a problem contacting the API.
        """
        try:
            resp = requests.get(type(self).POLLINATIONS_MODELS_URL, timeout=self.timeout)
            resp.raise_for_status()
            models = resp.json()
            if not isinstance(models, list):
                raise PollinationsError("Unexpected response format from models endpoint.")
            return models
        except Exception as e:
            raise PollinationsError(f"Failed to fetch models: {e}")
    
    def print_models_list(self):
        """
        Prints a formatted table of Pollinations models to the terminal.
        """

        models = self.list_models()

        if not models:
            print("No models found.")
            return

        # Define column headers
        headers = ["Name", "Description", "Provider", "Tier", "Vision"]
        print("{:<22} | {:<30} | {:<20} | {:<12} | {:<6}".format(*headers))
        print("-" * 103)

        for m in models:
            desc = m.get("description", "")
            if len(desc) > 28:
                desc = desc[:27] + "…"
            print("{:<22} | {:<30} | {:<20} | {:<12} | {:<6}".format(
                m.get("name", ""),
                desc,
                m.get("provider", ""),
                m.get("tier", ""),
                str(m.get("vision", False))
            ))