from re import split, sub
from os import path
from urllib.parse import urlparse


def get_file_path(dirty_path):
    """Clear the path from invalid characters and replace it to "-"

    Args:
        dirty_path (str): input path

    Returns:
        [str]: clear path, extension
    """
    clear_path = sub(r'https://|http://|.html', '', dirty_path)
    file_path, extension = path.splitext(clear_path)
    file_path_list = split(r'[\/\.\:]', file_path)
    clear_file_path_list = [world for world in file_path_list if world]
    spiked_name = '-'.join(clear_file_path_list)
    return spiked_name, extension
    

def is_not_out_link(link, url):
    """Сheck if the link is on or off the site.

    Args:
        link (str): local link
        url (str): page url

    Returns:
        bool: True / False
    """
    parsed_link = urlparse(link)
    parsed_url = urlparse(url)
    link_domain = parsed_link.netloc
    url_domain = parsed_url.netloc
    if link_domain:
        return link_domain == url_domain
    return parsed_link.path


def to_filename(path):
    """Filename frome path.

    Args:
        path (str): url

    Returns:
        str: file-name-extension
    """
    file_path, extension = get_file_path(path)
    print(file_path)
    print(extension)
    extension = '.html' if extension == '' else extension
    return '{0}{1}'.format(file_path, extension)


def to_foldername(path):
    """Filename frome path.

    Args:
        path (str): url

    Returns:
        str: folder-name-extension_files
    """
    file_path, _ = get_file_path(path)
    return '{0}_files'.format(file_path)


def to_page_filename(path):
    """Filename frome path.

    Args:
        path (str): url

    Returns:
        str: file-name.html
    """
    file_path, _ = get_file_path(path)
    return '{0}.html'.format(file_path)
