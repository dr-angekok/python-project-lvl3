"""Test module fore the page_loader."""
import tempfile
from os import path, popen

import page_loader
import pook
import pytest


def test_version():
    assert page_loader.__version__ == '0.1.0'


@pytest.mark.parametrize("link,exs", [
    ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    ('https://pythonworld.ru/moduli/modul-os-path.html', 'pythonworld-ru-moduli-modul-os-path.html'),
    ('http://pythonworld.ru/moduli/modul-os-path.html', 'pythonworld-ru-moduli-modul-os-path.html'),
    ('tproger.ru/translations/regular-expression-python', 'tproger-ru-translations-regular-expression-python.html'),
    ('tproger.ru/translations/regular-expression-python/', 'tproger-ru-translations-regular-expression-python.html')])

def test_get_name_for_page(link, exs):
    assert page_loader.page_loader.get_name_for_page(link) == exs


@pytest.mark.parametrize("link,exs,param1,param2", [
    ('https://pythonworld.ru/moduli/modul-os-path.html', 'pythonworld-ru-moduli-modul-os-path_files', True, False),
    ('https://pythonworld.ru/moduli/modul-os-path.png', 'pythonworld-ru-moduli-modul-os-path.png', False, True),
    ('pythonworld.ru/moduli/modul-os-path.jpg', 'pythonworld-ru-moduli-modul-os-path.jpg', False, True),])

def test_get_name_for(link,exs,param1,param2):
    assert page_loader.page_loader.get_name_for_page(link, is_folder=param1, is_files=param2) == exs
    assert page_loader.page_loader.get_name_for_page(link, is_folder=param1, is_files=param2) == exs


def test_cli_help_string():
    result = str(popen('poetry run page_loader -h').read())
    assert '-o OUTPUT, --output OUTPUT' in result
    assert 'positional arguments:\n  link' in result


@pook.on
def test_download_page():
    LINK_FOR_TEST = 'https://ru.wikipedia.org/wiki/Python'
    PATH_TO_FOLDER = tempfile.TemporaryDirectory()
    PATH_TO_PAGE = 'ru-wikipedia-org-wiki-Python.html'
    RESPONSE = {'found': 'body'}
    mock = pook.get(LINK_FOR_TEST, reply=200, response_json=RESPONSE)
    with PATH_TO_FOLDER as temp:
        page_loader.download(LINK_FOR_TEST, temp)
        assert mock.calls == 1
        assert path.isfile(path.join(temp, PATH_TO_PAGE))
