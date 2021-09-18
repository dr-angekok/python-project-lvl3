from page_loader.errors import SaveFileError, SavePageError
from os import path
import logging


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
        logging.info('Saving page at: {0}'.format(filename))
    except IOError:
        raise SavePageError('Path to saving page is not accessible.')


def save_file(path_to_file, content):
    try:
        with open(path_to_file, 'wb') as file:
            file.write(content)
        logging.info('Saved file {0}'.format(path_to_file))
    except IOError:
        raise SaveFileError('Path to saving "{0}" is not accessible.'.format(path_to_file))
