import openai
import backoff

from src.debugger import Debugger


class LLM:
    def __init__(self, config):
        self.config = config
        self.debugger = Debugger('debug.yml')

    def _parameters(self):
        return {
            **self.DEFAULT_PARAMETERS,
            **self.config.parameters
        }


class OpenAI(LLM):
    DEFAULT_PARAMETERS = {
        'model': 'gpt-4',
    }

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def complete(self, messages):
        parameters = self._parameters()
        self.debugger.record(messages, parameters)
        response = openai.ChatCompletion.create(
            **self._parameters(),
            messages=messages,
        )['choices'][0]['message']['content']
        self.debugger.record(messages, parameters, response)
        return response
