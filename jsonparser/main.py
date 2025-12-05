import argparse
import sys
from parser import Json
from lexical import Lexical


def get_args() -> tuple[argparse.Namespace, str]:
    parser = argparse.ArgumentParser(prog="JsonParser")
    parser.add_argument("file", nargs="?", default=None)
    args = parser.parse_args()
    if args.file:
        data = open(args.file, "r").read()
    else:
        data = sys.stdin.read()
    return (args, data)


def main():
    args, data = get_args()
    result = Json(data)
    print(result)


if __name__ == "__main__":
    main()
