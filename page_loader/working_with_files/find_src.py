from bs4 import BeautifulSoup


def check_src(src):
    if src is None:
        return False
    elif src.find('//') != -1 or src.find('?') != -1:
        return False
    return True


def find_src(file):
    soup = BeautifulSoup(file, features="html.parser")
    images = soup.find_all('img')
    list_of_images = []
    for image in images:
        src = image.get('src')
        if check_src(src):
            list_of_images.append(src)
    return list_of_images
