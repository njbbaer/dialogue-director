import sys
import argparse

from src.dialogue import Dialogue

parser = argparse.ArgumentParser()
parser.add_argument("config", help="location of the configuration file")
args = parser.parse_args()

Dialogue(args.config, interactive=True).loop()
