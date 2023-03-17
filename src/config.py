from src.yaml_setup import yaml


class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        self.reload()

    @property
    def agents(self):
        return self.content['agents']

    @property
    def initial_messages(self):
        return self.content['messages']

    @property
    def parameters(self):
        return self.content['parameters']

    def reload(self):
        with open(self.filepath, 'r') as f:
            self.content = yaml.load(f)

    def prompt(self, name):
        return self.agents[name]['prompt']
