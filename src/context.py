import os
import datetime
from ruamel.yaml.scalarstring import LiteralScalarString

from src.yaml_setup import yaml


class Context:
    def __init__(self, config):
        self.messages = config.initial_messages
        self.filepath = Context.generate_filepath(config.filepath)

    def reload(self,):
        with open(self.filepath, 'r') as f:
            self.messages = yaml.load(f)

    def save(self):
        with open(self.filepath, 'w') as f:
            yaml.dump(self.messages, f)

    def append_message(self, message):
        self.messages.append({
            message.author: LiteralScalarString(message.content)
        })
        self.save()

    @staticmethod
    def generate_filepath(filename):
        basename = os.path.basename(filename)
        name, ext = os.path.splitext(basename)
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        return f'contexts/{name}_{timestamp}{ext}'
