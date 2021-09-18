"""Load url to files."""
import logging
from os import path

import requests
from progress.bar import IncrementalBar

import page_loader.logging
from page_loader import url
from page_loader.errors import LoadPageError
from page_loader.html import prepare
from page_loader.storage import make_folder, save_file, save_page


def load_page(link):
    """Load page by link.

    Args:
        link (str): link to download page

    Raises:
        LoadPageError:

    Returns:
        str: loaded page
    """
    try:
        page = requests.get(link)
        page.raise_for_status()
        if page.encoding is None:
            page.encoding = 'utf-8'
    except (requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema):
        raise LoadPageError('Wrong page address.')
    except requests.exceptions.ConnectionError:
        raise LoadPageError('Connection error')
    except requests.exceptions.HTTPError:
        raise LoadPageError('Connection failed')
    return page.content


def save_files(link_chain, page_filename):
    """Saves link files within the page according to the link - file name chain.

    Args:
        link_chain (list): list chain (link, filename to save)
        page_filename (str): main page filename

    Raises:
        SaveFileError:
    """
    bar = IncrementalBar('Saving files  ', max=len(link_chain))
    for link, path_to_file in link_chain:
        if path_to_file != page_filename:
            try:
                source = requests.get(link, stream=True)
                source.raise_for_status()
                logging.info('Successful request from {0}'.format(link))
            except (requests.exceptions.InvalidSchema,
                    requests.exceptions.MissingSchema):
                bar.next()
                continue
            except requests.exceptions.ConnectionError:
                bar.next()
                continue
            except requests.exceptions.HTTPError:
                bar.next()
                continue
            save_file(path_to_file, source.content)
            bar.next()
    bar.finish()


def download(link, folder='', log_level='info'):
    """Loads a web page with accompanying files from a link.

    Args:
        link (str): Link to page to download.
        folder (str, optional): a folder to save page with files. Defaults to ''.
        log_level (str, optional): logging level: debug', 'info', 'warning', 'error', 'critical'. Defaults to 'info'.
    """
    page_loader.logging.setup(log_level)
    page = load_page(link)
    page_file_name = path.join(folder, url.to_page_filename(link))
    folder_name = url.to_foldername(link)
    path_to_folder = path.join(folder, folder_name)
    make_folder(path_to_folder)
    updated_page, page_files_links = prepare(page, link, path_to_folder, folder_name, page_file_name)
    save_page(page_file_name, updated_page)
    save_files(page_files_links, page_file_name)
    return page_file_name
