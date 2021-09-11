from page_loader.errors import LoadPageError, MakeDirError, SaveFileError, SavePageError
import requests
from os import mkdir, path


def save_page(filename, page):
    """Save page by filename.

    Args:
        filename (str):
        page (str):

    Raises:
        SavePageError:
    """
    if path.isfile(filename):
        raise SavePageError('Page "{0}" is present'.format(filename))
    try:
        with open(filename, "w") as file:
            file.write(page)
    except IOError:
        raise SavePageError('Path to saving page is not accessible.')


def make_folder(path_to_folder):
    """Make folder by path.

    Args:
        path_to_folder (str):

    Raises:
        MakeDirError: Raises if the path is not reachable or exists.
    """
    if path.isdir(path_to_folder):
        raise MakeDirError('Folder "{0}" is present'.format(path_to_folder))
    try:
        mkdir(path_to_folder)
    except IOError:
        raise MakeDirError('Path to making folder is not accessible.')
    
    
def save_file(path_to_file, content):
    try:
        with open(path_to_file, 'wb') as file:
            file.write(content)
    except IOError:
        raise SaveFileError('Path to saving "{0}" is not accessible.'.format(path_to_file))
