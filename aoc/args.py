import argparse
from pathlib import Path

DEBUG = False


def read_input() -> str:
    global DEBUG
    p = argparse.ArgumentParser()
    p.add_argument("input", nargs="?", default="input.txt")
    p.add_argument("-d", "--debug", action="store_true")
    args = p.parse_args()
    DEBUG = args.debug

    return Path(args.input).read_text().strip()
