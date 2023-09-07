import sys

from src.context import Context
from src.config import Config
from src.llm import OpenAI
from src.message import Message


class Dialogue:
    def __init__(self, config_filepath, interactive=False):
        self.config = Config(config_filepath)
        self.context = Context(self.config)
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
        message = Message.create(name, response, self.config.rlp_mode)
        self.context.append_message(message)
        message.print()
        return response

    def _render_messages(self, name):
        rendered_messages = [{'role': 'system', 'content': self.config.prompt(name)}]
        for message in self.context.messages:
            author, content = list(message.items())[0]
            message = Message.create(author, content, self.config.rlp_mode)
            rendered_message = message.render_message(name)
            rendered_messages.append(rendered_message)
        return rendered_messages

    def _pause(self):
        input("Press enter to continue...")
        sys.stdout.write("\033[F")  # Move the cursor up one line
        sys.stdout.write("\033[K")  # Clear the current line
        self.context.reload()
        self.config.reload()

