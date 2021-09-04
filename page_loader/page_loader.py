"""Load url to files."""
import logging
from os import mkdir, path
from re import split, sub

import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from urllib.parse import urlparse, urlunparse


class MakeDirError(Exception):
    pass


class SavePageError(Exception):
    pass


class LoadPageError(Exception):
    pass


class SaveFileError(Exception):
    pass


class LoadFileError(Exception):
    pass


def get_file_path(dirty_path):
    """Clear the path from invalid characters.

    Args:
        dirty_path (str): input path

    Returns:
        [str]: clear path
    """
    file_path_list = split(r'[\/\.\:]', dirty_path)
    clear_file_path_list = [world for world in file_path_list if world]
    return '-'.join(clear_file_path_list)


def get_name(page_path, is_folder=False, is_files=False, is_log=False):
    """Make file name frome path.

    Args:
        page_path (str): page path
        is_folder (bool, optional):. Defaults to False.
        is_files (bool, optional):. Defaults to False.
        is_log (bool, optional):. Defaults to False.

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
    elif is_log:
        return '{0}{1}'.format(get_file_path(file_path), '.log')
    return '{0}.html'.format(file_path)


def is_not_out_link(link, url):
    parsed_link = urlparse(link)
    parsed_url = urlparse(url)
    link_domain = parsed_link.netloc
    url_domain = parsed_url.netloc
    if link_domain:
        return link_domain == url_domain
    return parsed_link.path


def update_links(page, url, path_to_folder):
    """Redirects links within the page file to a local resource.

    Args:
        page (str): page for changes
        url (str): link to page
        path_to_folder (str): path to folder with files

    Returns:
        [str, tuple]: page and list of links chain
    """
    soup = BeautifulSoup(page, "html.parser")
    links = soup.find_all(["script", "img", "link"])
    link_chain = []
    bar = IncrementalBar('Updating links', max=len(links))
    for tag in links:
        for attr in ('href', 'src'):
            if attr in tag.attrs:
                link = tag[attr]
                if is_not_out_link(link, url):
                    logging.debug('sourse to update_link: {0}'.format((url, link, path_to_folder, tag, attr, link_chain)))
                    parsed_link = urlparse(link)
                    parsed_url = urlparse(url)
                    base = parsed_url.netloc
                    scheme = parsed_url.scheme
                    link = parsed_link.path
                    link = urlunparse((scheme, base, link, "", "", ""))
                    path_to_extra_file = path.join(path_to_folder, get_name(link, is_files=True))
                    logging.debug('updated_link: {0}'.format(path_to_extra_file))
                    tag[attr] = path_to_extra_file
                    link_chain.append((link, path_to_extra_file))
        bar.next()
    bar.finish()
    changed_page = soup.prettify('utf-8')
    return changed_page, link_chain


def save_files(link_chain):
    bar = IncrementalBar('Saving files  ', max=len(link_chain))
    for link, path_to_file in link_chain:
        try:
            source = requests.get(link, stream = True)
            source.raise_for_status()
        except (requests.exceptions.InvalidSchema,
                requests.exceptions.MissingSchema):
            raise LoadFileError('Wrong file address.')
        except requests.exceptions.ConnectionError:
            raise LoadFileError('Connection to load file error')
        except requests.exceptions.HTTPError:
            raise LoadFileError('Connection to load file {0} failed'.format(link))

        try:
            with open(path_to_file, 'wb') as file:
                file.write(source.content)
        except IOError:
            raise SaveFileError('Path to saving "{0}" is not accessible.'.format(path_to_file))
        bar.next()
    bar.finish()


def load_page(link):
    try:
        page = requests.get(link)
        page.raise_for_status()
    except (requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema):
        raise LoadPageError('Wrong page address.')
    except requests.exceptions.ConnectionError:
        raise LoadPageError('Connection error')
    except requests.exceptions.HTTPError:
        raise LoadPageError('Connection failed')
    return page.text


def save_page(filename, page):
    if path.isfile(filename):
        raise SavePageError('Page "{0}" is present'.format(filename))
    try:
        with open(filename, "wb") as file:
            file.write(page)
    except IOError:
        raise SavePageError('Path to saving page is not accessible.')


def make_folder(path_to_folder):
    if path.isdir(path_to_folder):
        raise MakeDirError('Folder "{0}" is present'.format(path_to_folder))
    try:
        mkdir(path_to_folder)
    except IOError:
        raise MakeDirError('Path to making folder is not accessible.')


def set_log_level(log_level, folder, link):
    """Sets the logging level.

    Args:
        log_level (str): logging level: debug, info, warning, error, critical.
        folder (str): a folder to save log file.
        link (str): Link to page.
    """
    logging_levels = {'debug': logging.DEBUG,
                      'warning': logging.WARNING,
                      'error': logging.ERROR,
                      'critical': logging.CRITICAL,
                      'info': logging.INFO}
    logging.basicConfig(filename=path.join(folder, get_name(link, is_log=True)),
                        filemode='w',
                        level=logging_levels[log_level])
    logging.info('Start')


def download(link, folder='', log_level='info'):
    """Loads a web page with accompanying files from a link.

    Args:
        link (str): Link to page to download.
        folder (str, optional): a folder to save page with files. Defaults to ''.
        log_level (str, optional): logging level: debug', 'info', 'warning', 'error', 'critical'. Defaults to 'info'.
    """
    set_log_level(log_level, folder, link)
    logging.info('Starting load page')
    bar = IncrementalBar('Loading page  ', max=3)
    page = load_page(link)
    bar.next()
    page_file_name = path.join(folder, get_name(link))
    logging.debug('page filename {0}'.format(page_file_name))
    folder_name = get_name(link, is_folder=True)
    logging.debug('folder name {0}'.format(folder_name))
    path_to_folder = path.join(folder, folder_name)
    logging.info('Making folder for files')
    bar.next()
    make_folder(path_to_folder)
    bar.next()
    bar.finish()
    logging.info('Starting link update')
    updated_page, page_files_links = update_links(page, link, path_to_folder)
    logging.info('Saving page')
    save_page(page_file_name, updated_page)
    logging.info('Saving accompanying files')
    logging.info('Files link count {0}'.format(len(page_files_links)))
    save_files(page_files_links)
    logging.info('All done')
    return page_file_name
