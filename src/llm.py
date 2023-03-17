import openai
import backoff


class LLM:
    def __init__(self, config):
        self.config = config


class OpenAI(LLM):
    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def complete(self, messages: str) -> str:
        return openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            **self.config.parameters,
            messages=messages,
        )['choices'][0]['message']['content']
