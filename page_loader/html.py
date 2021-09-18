from os import path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

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
    tags = soup.find_all(["script", "img", "link"])
    link_chain = []
    for tag in tags:
        for attr in ('href', 'src'):
            if attr in tag.attrs:
                resource_url = tag[attr]
                if url.is_local(resource_url, _url):
                    full_path_res_url = urljoin(_url, resource_url)
                    extra_file_name = url.to_filename(resource_url)
                    path_to_extra_file = path.join(path_to_folder, extra_file_name)

                    tag[attr] = path.join(folder_name, extra_file_name)
                    link_chain.append((full_path_res_url, path_to_extra_file))

    changed_page = soup.prettify()
    return changed_page, link_chain
