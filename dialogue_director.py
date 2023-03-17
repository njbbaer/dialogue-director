import sys

from src.conversation import Conversation

if __name__ == '__main__':
    filename = sys.argv[1]
    conversation = Conversation(filename)
    conversation.run()
