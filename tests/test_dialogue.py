from unittest import TestCase, mock
import textwrap
import os

from src.dialogue import Dialogue


class TestDialogue(TestCase):
    context_filename = 'test_context.yml'

    def read_context(self):
        with open(self.context_filename, 'r') as f:
            return f.read()

    @mock.patch('builtins.print')
    @mock.patch('openai.ChatCompletion.create')
    def test_run(self, mock_chat_completion, mock_print):
        mock_chat_completion.return_value = {
            'choices': [{'message': {'content': 'Hello, how can I assist you?'}}],
        }

        dialogue = Dialogue('configs/example.yml')
        dialogue.context.filename = self.context_filename
        dialogue.converse()

        self.assertEqual(self.read_context(), textwrap.dedent('''\
            - ALICE: |-
                Hello Bob, how are you?
            - BOB: |-
                I'm well Alice, thanks for asking. How are you?
            - ALICE: |-
                Hello, how can I assist you?
            - BOB: |-
                Hello, how can I assist you?
            '''))

    def tearDown(self):
        os.remove(self.context_filename)
