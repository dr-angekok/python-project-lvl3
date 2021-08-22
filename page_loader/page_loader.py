"""Load url to files."""
from os import path
from re import split, sub

import requests


def get_file_path(path):
    file_path_list = split(r'[\/\.]', path)
    clear_file_path_list = [world for world in file_path_list if world]
    file_path = '-'.join(clear_file_path_list)
    return file_path


def get_name_for_page(page_path, is_folder=False, is_files=False):
    """Make file name frome path.

    Args:
        page_path (str): page path

    Returns:
        str: filename
    """
    clear_path = sub(r'https://|http://|.html', '', page_path)
    file_path = get_file_path(clear_path)
    if is_folder:
        return '{0}_files'.format(file_path)
    elif is_files:
        file_path, extension = path.splitext(clear_path)
        return '{0}{1}'.format(get_file_path(file_path), extension)
    return '{0}.html'.format(file_path)


def load_page(link):
    page = requests.get(link)
    return page.text

def save_page(filename, page):
    with open(filename, "w") as file:
        file.write(page)


def download(link, folder=''):
    page = load_page(link)
    file_name = path.join(folder, get_name_for_page(link))
    save_page(file_name, page)



if __name__ == '__main__':
    print('is not a programm')
