import re
from os.path import splitext


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


def domain_only(url: str):
    schema_idx = url.find('://')
    schema = url[:schema_idx + 3]
    url = url[schema_idx + 3:]
    domain_end = url.find('/')
    url = url[:domain_end]
    return schema + url
