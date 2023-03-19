import os
import datetime
from ruamel.yaml.scalarstring import LiteralScalarString

from src.yaml_setup import yaml


class Context:
    def __init__(self, config):
        self.messages = config.initial_messages
        self.filename = Context.timestamp_filename(config.filename)

    def reload(self,):
        with open(self.filename, 'r') as f:
            self.messages = yaml.load(f)

    def save(self):
        with open(self.filename, 'w') as f:
            yaml.dump(self.messages, f)

    def append_message(self, name, message):
        self.messages.append({
            name: LiteralScalarString(message)
        })
        self.save()

    @staticmethod
    def timestamp_filename(filename):
        basename = os.path.basename(filename)
        name, ext = os.path.splitext(basename)
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        return f'{name}_{timestamp}{ext}'
