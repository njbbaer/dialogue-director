import sys

from src.context import Context
from src.config import Config
from src.llm import OpenAI


class Dialogue:
    def __init__(self, filepath, interactive=False):
        self.config = Config(filepath)
        self.context = Context(self.config.initial_messages)
        self.llm = OpenAI(self.config)
        self.interactive = interactive

    def loop(self):
        while True:
            self.converse()

    def converse(self):
        for name in self.config.agents:
            self._speak(name)
            if self.interactive:
                self._pause()

    def _speak(self, name):
        rendered_messages = self._render_messages(name)
        response = self.llm.complete(rendered_messages)
        self.context.append_message(name, response)
        print(f'{name}: {response}\n')
        return response

    def _render_messages(self, name):
        rendered_messages = [{'role': 'system', 'content': self.config.prompt(name)}]
        for message in self.context.messages:
            name_, content = list(message.items())[0]
            role = 'assistant' if name_ == name else 'user'
            rendered_messages.append({'role': role, 'content': content})
        return rendered_messages

    def _pause(self):
        input("Press enter to continue...")
        sys.stdout.write("\033[F")  # Move the cursor up one line
        sys.stdout.write("\033[K")  # Clear the current line
        self.context.reload()
        self.config.reload()
