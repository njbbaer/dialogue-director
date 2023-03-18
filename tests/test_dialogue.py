from unittest import TestCase, mock
import textwrap

from src.dialogue import Dialogue


def read_context():
    with open('context.yml', 'r') as f:
        return f.read()


class TestDialogue(TestCase):
    @mock.patch('builtins.print')
    @mock.patch('openai.ChatCompletion.create')
    def test_run(self, mock_chat_completion, mock_print):
        mock_chat_completion.return_value = {
            'choices': [{'message': {'content': 'Hello, how can I assist you?'}}],
        }

        Dialogue('example.yml').converse()

        self.assertEqual(read_context(), textwrap.dedent('''\
            - ALICE: |-
                Hello Bob, how are you?
            - BOB: |-
                I'm well Alice, thanks for asking. How are you?
            - ALICE: |-
                Hello, how can I assist you?
            - BOB: |-
                Hello, how can I assist you?
            '''))
