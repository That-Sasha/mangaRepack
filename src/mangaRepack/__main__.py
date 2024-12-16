from argparse import ArgumentParser
from importlib import resources
from pydoc import locate
import tomli

parser = ArgumentParser()

def main():
    # Set up cli arguments
    config = tomli.loads(resources.read_text("mangaRepack", "config.toml", encoding="utf-8"))
    
    arguments_dict = config["arguments"].items()

    for _, arg in arguments_dict:
        parser.add_argument(
            *arg.get("name"), 
            action=arg.get("action", "store"),
            type=locate(arg.get("type", "str")),
            dest=arg.get("dest"),
            metavar=arg.get("metavar", None),
            help=arg.get("help", None)
        )
    
    args = vars(parser.parse_args())