"""Test module fore the page_loader."""
from os import path

import page_loader
import pook


def make_path(file):
    PATH = 'tests/fixtures/'
    return '{0}{1}'.format(PATH, file)


def read_out_exs(filename):
    with open(make_path(filename), 'r') as file:
        out = file.read()
    return str(out)


def test_version():
    assert page_loader.__version__ == '0.1.0'


@pook.on
def test_download_page(tmpdir):
    PAGE_LINK_FOR_TEST = 'https://ru.wikipedia.org/wiki/Python'
    IMAGE_LINK_FOR_TEST = 'https://ru.wikipedia.org/assets/professions/nodejs.png'
    PATH_TO_FOLDER = tmpdir
    PATH_TO_PAGE = 'ru-wikipedia-org-wiki-Python.html'
    PAGE_RESPONSE = read_out_exs('input_page.html')

    page_mock = pook.get(PAGE_LINK_FOR_TEST, reply=200,
                         response_body=PAGE_RESPONSE, response_headers={'Content-Type': 'text'})
    image_mock = pook.get(IMAGE_LINK_FOR_TEST, reply=200,
                          response_body=PAGE_RESPONSE, response_headers={'Content-Type': 'pook'})
    page_loader.download(PAGE_LINK_FOR_TEST, PATH_TO_FOLDER)
    assert page_mock.calls == 1
    assert path.isfile('{0}/{1}'.format(PATH_TO_FOLDER, PATH_TO_PAGE))
    assert image_mock.calls == 1
