from argparse import ArgumentParser, FileType
from glob import glob 
from importlib import resources
from pydoc import locate
import tomli
import re

from mangaRepack import repack

parser = ArgumentParser(
            usage="%(prog)s [options] files")

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

    # Add file mandatory positional path arg
    parser.add_argument('file_paths', nargs='+', metavar="files")

    args = parser.parse_args()
    
    # Handle wild cards
    file_paths = []
    for arg in args.file_paths:  
        possible_path = glob(arg)
        
        # Match only .cbz files using regex
        if len(possible_path) > 0 and re.findall(r"^.*.cbz$", possible_path[0]):
            file_paths += possible_path
    
    # Exit if no valid files found
    if len(file_paths) > 0:
        repack.repack(file_paths)
    else:
        print("No matching .cbz files found")
        return
    
