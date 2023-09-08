from src.yaml_setup import yaml


class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        self.reload()

    @property
    def agents(self):
        return self.config['agents']

    @property
    def initial_messages(self):
        return self.config.get('messages') or []

    @property
    def parameters(self):
        return self.config.get('parameters') or {}

    def reload(self):
        with open(self.filepath, 'r') as f:
            self.config = yaml.load(f)

    def get_prompt(self, name):
        return self.agents[name]['prompt']

    def get_message_type(self, name):
        return self.agents[name].get('type') or 'normal'
