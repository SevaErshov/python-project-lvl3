#!usr/bit/env python3
import re
import requests
import argparse
from os import getcwd, mkdir
from os.path import splitext
from bs4 import BeautifulSoup


def name(url: str):
    schema_idx = url.find('://')
    url = url[schema_idx + 3:]
    path, ext = splitext(url)
    if ext == '.html':
        url = path
    url = re.split(r'\W+', url)
    url = '-'.join(url)
    return url


def name_pic(url: str, src: str, directory: str):
    path, _ = splitext(src)
    file_name = re.split(r'\W+', path[1:])
    file_name = '-'.join(file_name) + '.png'
    file_name = name(url) + '-' + file_name
    return directory + '/' + file_name


def download_pics(url: str, src: str, directory: str, file):
    if url[-1] == '/':
        url = url[:len(url) - 1]
    img = requests.get(url + src)
    path_storage = name_pic(url, src, directory)
    img_storage = open(path_storage, 'wb')
    img_storage.write(img.content)
    img_storage.close()
    return path_storage


def edit_html(path, url, directory):
    file = open(path)
    soup = BeautifulSoup(file, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        new_src = name_pic(url, image.get('src'), directory)
        image['src'] = new_src
    to_write = soup.prettify()
    file.close()
    file = open(path, 'w')
    file.write(to_write)


def find_src(file):
    soup = BeautifulSoup(file, features="html.parser")
    images = soup.find_all('img')
    if images == []:
        return None
    return [img.get('src') for img in images if img.get('src')[0] == '/'] #костыли наше всё


def download(url: str, dirname=None):
    if dirname is None or dirname == 'current':
        dirname = getcwd()
    path = dirname + '/' + name(url) + '.html'
    info = requests.get(url).text
    file = open(path, "w+")
    file.write(info)
    file.close()
    file = open(path)
    images = find_src(file)
    if images is None:
        return path
    dir_files = name(url) + '_files'
    directory = dirname + '/' + dir_files
    mkdir(directory)
    for image in images:
        download_pics(url, image, directory, file)
    edit_html(path, url, dir_files)
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
