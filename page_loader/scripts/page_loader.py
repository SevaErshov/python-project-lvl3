#!usr/bit/env python3
import argparse
from page_loader.downloading.download import download
from page_loader.logger import InternalError, logger
from sys import exit


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('url')
        parser.add_argument('--output', '-o', default="current")
        args = parser.parse_args()
        path = download(args.url, args.output)
        print(path)
    except InternalError as e:
        logger.error(e)
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    main()
