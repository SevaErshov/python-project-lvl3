import requests
from os import getcwd
from os.path import exists
from page_loader.working_with_files import find_src, download_files
from page_loader.naming.give_name import path_name
from page_loader.logger import logger, InternalError


def create_html_page(url, path):
    info = requests.get(url).text
    file = open(path, "w+")
    file.write(info)
    file.close()
    logger.info('HTML-page was created')


def download(url: str, dirname=None):
    if dirname is None or dirname == 'current':
        dirname = getcwd()

    if not exists(dirname):
        logger.error(f'Directory \'{dirname}\' doesn\'t exist')
        raise InternalError('Directory doesn\'t exist')

    path = path_name(url, dirname)
    logger.info(f'Start downloading \'{url}\' to \'{path}\'')
    create_html_page(url, path)
    file = open(path)
    files = find_src(file, url)
    file.close()
    if files is None or files == []:
        logger.info('Downloading completed!')
        return path
    download_files(url, dirname, path, files)
    logger.info('Downloading completed!')
    return path
