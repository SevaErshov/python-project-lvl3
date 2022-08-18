import requests
from bs4 import BeautifulSoup
from os import mkdir
from page_loader.naming.give_name import name, name_file, domain_only
from page_loader.working_with_files.find_files import edit_format, check_format
from os.path import splitext
from urllib.parse import urlparse


def download_tags(url: str, tag: str, directory: str):
    if url[-1] == '/':
        url = url[:len(url) - 1]
    path_storage = name_file(url, tag, directory)
    parser = urlparse(path_storage)
    url_parser = urlparse(url)

    if splitext(path_storage)[1] == '.html' and parser[1] == url_parser[1]:
        storage = open(path_storage, 'w+')
        file = requests.get(domain_only(url) + tag).text
        storage.write(file)
        storage.close()
        return path_storage

    file = requests.get(domain_only(url) + tag)
    img_storage = open(path_storage, 'wb')
    img_storage.write(file.content)
    img_storage.close()
    return path_storage


def edit_path(files, tag, url, directory):
    for file in files:
        edited_tag = edit_format(file.get(tag), url)
        if check_format(edited_tag):
            new_src = name_file(url, edited_tag, directory)
            file[tag] = new_src


def edit_html(path, url, directory):
    file = open(path)
    soup = BeautifulSoup(file, 'html.parser')
    images = soup.find_all('img')
    images.extend(soup.find_all('script'))
    edit_path(images, 'src', url, directory)
    links = soup.find_all('link')
    edit_path(links, 'href', url, directory)
    to_write = soup.prettify()
    file.close()
    file = open(path, 'w')
    file.write(to_write)


def download_files(url: str, dirname: str, path: str, files: list):
    dir_files = name(url) + '_files'
    directory = dirname + '/' + dir_files
    mkdir(directory)
    for tag in files:
        download_tags(url, tag, directory)
    edit_html(path, url, dir_files)
