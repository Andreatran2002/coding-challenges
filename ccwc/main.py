
import argparse
import re
import sys


def parse_args():
    parser = argparse.ArgumentParser(
                    prog='CCWC',
                    description='Count word')
    parser.add_argument('file',nargs='?',default=None)
    parser.add_argument("-c", "--count", action="store_true")
    parser.add_argument("-w", "--word", action="store_true")
    parser.add_argument("-l", "--line", action="store_true")
    parser.add_argument("-m", "--locale", action="store_true")
    
    return parser.parse_args()

def main():

    args = parse_args()

    if args.file: 
        data = open(args.file, 'rb').read()
    else: 
        data = sys.stdin.buffer.read()
    
    if args.count: 
        print(len(data))
    if args.word: 
        print(len(re.findall(r"\S+", data.decode() )))
    if args.line: 
        print(len(re.findall(r'\n', data.decode() )))
    if args.locale: 
        print(len(data.decode()))

if __name__ == "__main__":
    main()