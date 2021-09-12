import logging
from os import path
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader import url


def prepare(page, _url, path_to_folder, folder_name, page_file_name):
    """Redirects links within the page file to a local resource.

    Args:
        page (str): page for changes
        _url (str): link to page
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
                if url.is_not_out_link(link, _url):
                    logging.debug('sourse to update_link: {0}'.format((_url, link, folder_name, tag, attr)))
                    parsed_link = urlparse(link)
                    link_base, link_path = parsed_link.netloc, parsed_link.path
                    parsed_url = urlparse(_url)
                    scheme = parsed_url.scheme
                    url_base, url_path = parsed_url.netloc, parsed_url.path
                    link = urlunparse((scheme, url_base, link_path, '', '', ''))
                    if url_base + url_path == link_base + link_path:
                        logging.debug('path_to_link: {0}'.format(page_file_name))
                        tag[attr] = page_file_name
                        logging.debug('tag[attr]: {0}'.format(tag[attr]))
                        link_chain.append((link, page_file_name))
                    else:
                        extra_file_name = url.to_filename(link)
                        path_to_extra_file = path.join(path_to_folder, extra_file_name)
                        path_to_update_file_link = path.join(folder_name, extra_file_name)
                        logging.debug('path_to_link: {0}'.format(path_to_extra_file))
                        logging.debug('updated_link: {0}'.format(path_to_update_file_link))
                        tag[attr] = path_to_update_file_link
                        logging.debug('tag[attr]: {0}'.format(tag[attr]))
                        link_chain.append((link, path_to_extra_file))
        bar.next()
    bar.finish()
    changed_page = soup.prettify(formatter='html5')
    return changed_page, link_chain
