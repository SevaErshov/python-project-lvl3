#!usr/bit/env python3
import requests
import argparse
from os import getcwd
from page_loader.working_with_files import find_src, download_files
from page_loader.naming.give_name import name


def create_html_page(url, dirname):
    path = dirname + '/' + name(url) + '.html'
    info = requests.get(url).text
    file = open(path, "w+")
    file.write(info)
    file.close()
    return path


def download(url: str, dirname=None):
    if dirname is None or dirname == 'current':
        dirname = getcwd()
    path = create_html_page(url, dirname)
    file = open(path)
    files = find_src(file, url)
    file.close()
    if files is None or files == []:
        return path
    download_files(url, dirname, path, files)
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
