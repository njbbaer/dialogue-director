import os
import datetime

from src.yaml_setup import yaml
from src.message import Message


class Context:
    def __init__(self, config):
        self.messages = [Message.from_dict(item) for item in config.initial_messages]
        self.filepath = Context.generate_filepath(config.filepath)
        self.save()

    def reload(self):
        with open(self.filepath, 'r') as f:
            yaml_data = yaml.load(f)
            self.messages = [Message.from_dict(item) for item in yaml_data]

    def save(self):
        with open(self.filepath, 'w') as f:
            yaml_data = [message.to_dict() for message in self.messages]
            yaml.dump(yaml_data, f)

    def append_message(self, message):
        self.messages.append(message)
        self.save()

    @staticmethod
    def generate_filepath(filename):
        basename = os.path.basename(filename)
        name, ext = os.path.splitext(basename)
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        return f'contexts/{name}_{timestamp}{ext}'
