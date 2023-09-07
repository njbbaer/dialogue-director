from ruamel.yaml.scalarstring import LiteralScalarString

from src.yaml_setup import yaml


class Debugger:
    def __init__(self, filepath):
        self.filepath = filepath

    def record(self, messages, parameters, response=None):
        with open(self.filepath, 'w') as file:
            yaml.dump({
                'parameters': parameters,
                'messages': [Debugger.format_message(message) for message in messages],
                'response': LiteralScalarString(response)
            }, file)

    @staticmethod
    def format_message(message):
        return {
            **message,
            'content': LiteralScalarString(message['content'])
        }
