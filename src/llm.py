import openai
import backoff


class LLM:
    def __init__(self, config):
        self.config = config

    def _parameters(self):
        return {
            **self.DEFAULT_PARAMETERS,
            **self.config.parameters
        }


class OpenAI(LLM):
    DEFAULT_PARAMETERS = {
        'model': 'gpt-3.5-turbo',
    }

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def complete(self, messages: str) -> str:
        return openai.ChatCompletion.create(
            **self._parameters(),
            messages=messages,
        )['choices'][0]['message']['content']
