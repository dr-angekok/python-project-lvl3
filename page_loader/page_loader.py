"""Load url to files."""
from os import path
from re import split, sub

import requests


def get_name_for_page(page_path):
    """Make file name frome path.

    Args:
        page_path (str): page path

    Returns:
        str: filename
    """
    clear_path = sub(r'https://|http://|.html', '', page_path)
    file_path_list = split(r'[\/\.]', clear_path)
    clear_file_path_list = [world for world in file_path_list if world]
    file_path = '-'.join(clear_file_path_list)
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
