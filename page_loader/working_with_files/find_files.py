from bs4 import BeautifulSoup
from urllib.parse import urlparse


def check_format(src):
    if src is None:
        return False
    elif src.find('//') != -1 or src.find('?') != -1:
        return False
    elif src.find(':') != -1:
        return False
    return True


def edit_format(src, url):
    if src is None:
        return src
    if src.find('//') != -1:
        src_parser = urlparse(src)
        parser = urlparse(url)
        if parser[1] == src_parser[1]:
            src = ''.join(src_parser[2:])
    return src


def find_container(containers, tag, url):
    list_of_files = []
    for container in containers:
        src = edit_format(container.get(tag), url)
        if check_format(src):
            list_of_files.append(src)
    return list_of_files


def find_src(file, url):
    soup = BeautifulSoup(file, features="html.parser")
    images = soup.find_all('img')
    scripts = soup.find_all('script')
    links = soup.find_all('link')
    images.extend(scripts)
    list_of_files = find_container(images, 'src', url)
    list_of_files.extend(find_container(links, 'href', url))
    return list_of_files
