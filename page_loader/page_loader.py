"""Load url to files."""
import logging
from os import mkdir, path

import requests
from progress.bar import IncrementalBar

import page_loader.logging
from page_loader import url as _url
from page_loader.html import prepare
from page_loader.storage import save_file, save_page


def download_resource(url):
    """Load resource by url.

    Args:
        link (str): link to download page

    Returns:
        str: loaded page
    """
    resource = requests.get(url)
    resource.raise_for_status()
    if resource.encoding is None:
        resource.encoding = 'utf-8'
    return resource.content


def download_resources(resurses, page_filename, path_to_folder):
    """Saves link files within the page according to the link - file name chain.

    Args:
        resurses (list): list chain (link, filename to save)
        page_filename (str): main page filename

    Raises:
        SaveFileError:
    """
    if not resurses:
        return

    if not path.exists(path_to_folder):
        mkdir(path_to_folder)

    bar = IncrementalBar('Saving files  ', max=len(resurses))
    for link, path_to_file in resurses:
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


def download(url, folder='', log_level='info'):
    """Loads a web page with accompanying files from a link.

    Args:
        link (str): Link to page to download.
        folder (str, optional): a folder to save page with files. Defaults to ''.
        log_level (str, optional): logging level: debug', 'info', 'warning', 'error', 'critical'. Defaults to 'info'.
    """
    page_loader.logging.setup(log_level)
    page = download_resource(url)
    page_file_name = path.join(folder, _url.to_page_filename(url))
    folder_name = _url.to_foldername(url)
    path_to_folder = path.join(folder, folder_name)
    updated_page, page_files_links = prepare(page, url, path_to_folder, folder_name, page_file_name)
    save_page(page_file_name, updated_page)

    download_resources(page_files_links, page_file_name, path_to_folder)
    return page_file_name
