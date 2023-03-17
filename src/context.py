from ruamel.yaml.scalarstring import LiteralScalarString

from src.yaml_setup import yaml


class Context:
    CONTEXT_FILE = 'context.yml'

    def __init__(self, messages):
        self.messages = messages

    def reload(self,):
        with open(self.CONTEXT_FILE, 'r') as f:
            self.messages = yaml.load(f)

    def save(self):
        with open(self.CONTEXT_FILE, 'w') as f:
            yaml.dump(self.messages, f)

    def append_message(self, name, message):
        self.messages.append({
            name: LiteralScalarString(message)
        })
        self.save()
