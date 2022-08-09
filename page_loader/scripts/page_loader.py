#!usr/bit/env python3
import re
import requests
import argparse
from os import getcwd


def name(url: str):
    schema_idx = url.find('://')
    url = url[schema_idx + 3:]
    url = re.split(r'\W+', url)
    url = '-'.join(url) + '.html'
    return url


def download(url: str, dirname=None):
    if dirname is None or dirname == 'current':
        dirname = getcwd()
    path = dirname + '/' + name(url)
    info = requests.get(url).text
    file = open(path, "w")
    file.write(info)
    file.close()
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--output', '-o', default="current")
    args = parser.parse_args()
    path = download(args.url, args.output)
    print(path)


if __name__ == "__main__":
    main()
