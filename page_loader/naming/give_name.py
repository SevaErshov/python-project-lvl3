import re
from os.path import splitext
from urllib.parse import urlparse


def name(url: str):
    url = ''.join(urlparse(url)[1:])
    path, ext = splitext(url)
    if ext == '.html':
        url = path
    url = re.split(r'\W+', url)
    url = '-'.join(url)
    return url


def name_file(url: str, src: str, directory: str):
    path, ext = splitext(src)
    if ext == '':
        ext = '.html'
    file_name = re.split(r'\W+', path[1:])
    file_name = '-'.join(file_name) + ext  # + '.png'
    url = ''.join(urlparse(url)[0] + '://' + urlparse(url)[1])
    file_name = name(url) + '-' + file_name
    return directory + '/' + file_name


def domain_only(url: str):
    parser = urlparse(url)
    schema = parser[0] + '://'
    domain = parser[1]
    return schema + domain
