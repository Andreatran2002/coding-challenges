
import argparse
import re
import sys

from app.controllers.compressor import Compressor


def parse_args():
    parser = argparse.ArgumentParser(
                    prog='Compressor',
                    description='Compress data')
    parser.add_argument('file')
    return parser.parse_args()

def main():
    args = parse_args()
    compressor = Compressor()
    compressor.process(args.file)

if __name__ == "__main__":
    main()