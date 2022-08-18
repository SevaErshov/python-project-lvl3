import requests
from bs4 import BeautifulSoup
from os import mkdir
from page_loader.naming.give_name import name, name_pic, domain_only


def download_pics(url: str, src: str, directory: str):
    if url[-1] == '/':
        url = url[:len(url) - 1]
    img = requests.get(domain_only(url) + src)
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


def download_files(url: str, dirname: str, path: str, srcs: list):
    dir_files = name(url) + '_files'
    directory = dirname + '/' + dir_files
    mkdir(directory)
    for image in srcs:
        download_pics(url, image, directory)
    edit_html(path, url, dir_files)
