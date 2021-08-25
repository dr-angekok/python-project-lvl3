"""Load url to files."""
from os import mkdir, path
from re import split, sub

import magic
from bs4 import BeautifulSoup
from requests import get as request_get


def get_file_path(dirty_path):
    """Clear the path from invalid characters.

    Args:
        dirty_path (str): input path

    Returns:
        [str]: clear path
    """
    file_path_list = split(r'[\/\.]', dirty_path)
    clear_file_path_list = [world for world in file_path_list if world]
    return '-'.join(clear_file_path_list)


def get_name(page_path, is_folder=False, is_files=False):
    """Make file name frome path.

    Args:
        page_path (str): page path
        is_folder (bool, optional):. Defaults to False.
        is_files (bool, optional):. Defaults to False.

    Returns:
        [str]: clear name for page or file
    """
    clear_path = sub(r'https://|http://|.html', '', page_path)
    file_path = get_file_path(clear_path)
    if is_folder:
        return '{0}_files'.format(file_path)
    elif is_files:
        file_path, extension = path.splitext(clear_path)
        return '{0}{1}'.format(get_file_path(file_path), extension)
    return '{0}.html'.format(file_path)


def is_not_out_link(link):
    return all(not link.startswith(prefix) for prefix in ['www', 'http'])


def make_update_link(url, link, path_to_folder, tag, attr, link_chain):
    link = link.lstrip('/')
    file_path = path.join(url, link)
    path_to_extra_file = path.join(path_to_folder, get_name(file_path, is_files=True))
    tag[attr] = path_to_extra_file
    link_chain.append((file_path, path_to_extra_file))


def update_links(page, url, path_to_folder):
    soup = BeautifulSoup(page, "lxml")
    links = soup.find_all(["script", "img", "link"])
    link_chain = []
    for tag in links:
        for attr in ('href', 'src'):
            if attr in tag.attrs:
                link = tag[attr]
                if is_not_out_link(link):
                    make_update_link(url, link, path_to_folder, tag, attr, link_chain)
    changed_page = soup.prettify('utf-8')
    return changed_page, link_chain


def save_files(source):
    for link, path_to_file in source:
        sourse = request_get(link)
        mime_type = magic.from_buffer(sourse.content, mime=True)
        TEXT_CONTENT = ('w', sourse.text)
        text_types = {'text/html':TEXT_CONTENT,
                      'text/css':TEXT_CONTENT,
                      'text/javascript':TEXT_CONTENT}
        mode, data = text_types.get(mime_type, ('wb', sourse.content))
        with open(path_to_file, mode) as file:
            file.write(data)


def load_page(link):
    page = request_get(link)
    return page.text

def save_page(filename, page):
    with open(filename, "wb") as file:
        file.write(page)


def download(link, folder=''):
    page = load_page(link)
    page_file_name = path.join(folder, get_name(link))
    folder_name = get_name(link, is_folder=True)
    path_to_folder = path.join(folder, folder_name)
    mkdir(path_to_folder)
    updated_page, page_files_links = update_links(page, link, path_to_folder)
    save_page(page_file_name, updated_page)
    save_files(page_files_links)
