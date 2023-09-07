import re


class Message:
    def __init__(self, author, content):
        self.author = author
        self.content = content

    def create(author, content, rlp_mode):
        if rlp_mode:
            return RLPMessage(author, content)
        else:
            return Message(author, content)

    def render_message(self, perspetive):
        return {
            'role': 'assistant' if perspetive == self.author else 'user',
            'content': self._render_content(perspetive)
        }

    def print(self):
        print(f'{self.author}: {self.content}')

    def _render_content(self, perspective):
        return self.content


class RLPMessage(Message):
    def __init__(self, author, content):
        super().__init__(author, content)
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
