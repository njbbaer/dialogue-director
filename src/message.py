import re
from ruamel.yaml.scalarstring import LiteralScalarString


class Message:
    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.message_type = 'normal'

    @staticmethod
    def create(author, content, message_type):
        if message_type == 'rlp':
            return RLPMessage(author, content)
        else:
            return Message(author, content)

    @staticmethod
    def from_dict(data):
        return Message.create(data['author'], data['content'], data.get('type'))

    def to_dict(self):
        return {
            'author': self.author,
            'type': self.message_type,
            'content': LiteralScalarString(self.content)
        }

    def render_message(self, perspetive):
        return {
            'role': 'assistant' if perspetive == self.author else 'user',
            'content': self._render_content(perspetive)
        }

    def print(self):
        print(f'{self.author}: {self.content}\n')

    def _render_content(self, _):
        return self.content


class RLPMessage(Message):
    def __init__(self, author, content):
        super().__init__(author, content)
        self.message_type = 'rlp'
        self.rlp_schema = [
            {
                'name': 'THINKS',
                'regex': r'<THINKS>(.*?)</THINKS>',
                'required': True,
                'private': True,
            },
            {
                'name': 'SPEAKS',
                'regex': r'<SPEAKS>(.*?)</SPEAKS>',
                'required': True,
                'private': False,
            },
            {
                'name': 'ANALYZES',
                'regex': r'<ANALYZES>(.*?)</ANALYZES>',
                'required': True,
                'private': True,
            },
            {
                'name': 'ACTS',
                'regex': r'<ACTS>(.*?)</ACTS>',
                'required': False,
                'private': False,
            },
        ]
        self._validate()

    def print(self):
        print(f'##### {self.author} ######')
        for component in self.rlp_schema:
            if not component['private']:
                match = re.search(component['regex'], self.content, re.DOTALL)
                if (match):
                    print(f'> {component["name"]}: {match.group(1)}')
        print()

    def _validate(self):
        for component in self.rlp_schema:
            if component['required'] and not re.search(component['regex'], self.content, re.DOTALL):
                raise Exception(f'Component {component["name"]} is required')

    def _render_content(self, perspective):
        if perspective == self.author:
            return self.content
        else:
            return self._get_filtered_content()

    def _get_filtered_content(self):
        filtered_components = self.content
        for component in self.rlp_schema:
            if component['private']:
                filtered_components = re.sub(component['regex'], '', filtered_components, flags=re.DOTALL)
        return filtered_components.strip()
