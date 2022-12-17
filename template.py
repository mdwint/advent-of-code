import argparse
from pathlib import Path

DEBUG = False


def main():
    global DEBUG
    p = argparse.ArgumentParser()
    p.add_argument("input", nargs="?", default="input.txt")
    p.add_argument("-d", "--debug", action="store_true")
    args = p.parse_args()
    DEBUG = args.debug

    text = Path(args.input).read_text().strip()
    print(text)

    print("Part 1:", 0)
    print("Part 2:", 0)


if __name__ == "__main__":
    main()
