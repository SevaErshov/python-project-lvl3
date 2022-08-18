from bs4 import BeautifulSoup
from urllib.parse import urlparse


def check_src(src):
    if src is None:
        return False
    elif src.find('//') != -1 or src.find('?') != -1:
        return False
    return True


def edit_src(src, url):
    if src is None:
        return src
    if src.find('//') != -1:
        src_parser = urlparse(src)
        parser = urlparse(url)
        if parser[1] == src_parser[1]:
            src = ''.join(src_parser[2:])
    return src


def find_src(file, url):
    soup = BeautifulSoup(file, features="html.parser")
    images = soup.find_all('img')
    list_of_images = []
    for image in images:
        src = edit_src(image.get('src'), url)
        if check_src(src):
            list_of_images.append(src)
    return list_of_images
