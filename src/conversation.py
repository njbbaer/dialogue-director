import sys

from src.context import Context
from src.config import Config
from src.llm import OpenAI


class Conversation:
    def __init__(self, filepath):
        self.config = Config(filepath)
        self.context = Context(self.config.initial_messages)
        self.llm = OpenAI(self.config)

    def run(self):
        while True:
            for name in self.config.agents:
                self._speak(name)
                self._pause()

    def _speak(self, name):
        rendered_messages = self._render_messages(name)
        response = self.llm.complete(rendered_messages)
        print(f'{name}: {response}\n')
        self.context.append_message(name, response)
        return response

    def _render_messages(self, name):
        rendered_messages = [{
            'role': 'system',
            'content': self.config.prompt(name)
        }]
        for message in self.context.messages:
            name_, content = list(message.items())[0]
            rendered_messages.append({
                'role': 'assistant' if name_ == name else 'user',
                'content': content
            })
        return rendered_messages

    def _pause(self):
        input("Press enter to continue...")
        sys.stdout.write("\033[F")  # Move the cursor up one line
        sys.stdout.write("\033[K")  # Clear the current line
        self.context.reload()
        self.config.reload()
