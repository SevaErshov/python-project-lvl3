import requests
from os import getcwd
from os.path import exists
from page_loader.working_with_files import find_src, download_files
from page_loader.naming.give_name import path_name
from page_loader.logger import logger, InternalError, ResponseError


def create_html_page(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        info = response.text
        file = open(path, "w+")
        file.write(info)
        file.close()
        logger.info('HTML-page was created')
    else:
        trace_error(response.status_code, url)


def trace_error(status_code, url):
    if status_code == 404:
        raise ResponseError(f'Page \'{url}\' doesn\'t exist!')
    elif status_code >= 300 and status_code < 400:
        raise ResponseError('A redirect was occured!')
    elif status_code == 204:
        raise ResponseError(f'There is no content in the page {url}!')
    elif status_code == 401:
        raise ResponseError('You are unauthorized on this resource!')
    elif status_code == 403:
        raise ResponseError('You do not have access to this resource!')
    else:
        raise ResponseError('Status code is not equal to 200')


def download(url: str, dirname=None):
    if dirname is None or dirname == 'current':
        dirname = getcwd()

    if not exists(dirname):
        raise InternalError(f'Directory \'{dirname}\' doesn\'t exist')

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
