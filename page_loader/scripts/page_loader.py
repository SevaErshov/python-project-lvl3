#!usr/bit/env python3
import requests
import argparse
from os import getcwd
from page_loader.working_with_files import find_src, download_files
from page_loader.naming.give_name import name
import logging
from os.path import exists


logging.basicConfig(level='DEBUG')
logger = logging.getLogger()

logging.getLogger('urllib3').setLevel('CRITICAL')


def create_html_page(url, dirname):
    path = dirname + '/' + name(url) + '.html'
    info = requests.get(url).text
    file = open(path, "w+")
    file.write(info)
    file.close()
    return path


def check_dirname(dirname):
    if not exists(dirname):
        logger.exception(f'Directory \'{dirname}\' doesn\'t exist!')


def download(url: str, dirname=None):
    logger.info(f'requested url: {url}')
    if dirname is None or dirname == 'current':
        dirname = getcwd()
    check_dirname(dirname)
    logger.info(f'output path: {dirname}')
    path = create_html_page(url, dirname)
    file = open(path)
    files = find_src(file, url)
    file.close()
    if files is None or files == []:
        return path
    download_files(url, dirname, path, files)
    logger.info(f'Page was downloaded as \'{dirname}\'')
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
