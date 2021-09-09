"""Test module fore the page_loader."""
from os import path, popen, listdir

import page_loader
import pook
import pytest


def make_path(file):
    PATH = 'tests/fixtures/'
    return '{0}{1}'.format(PATH, file)


def read_out_exs(filename):
    with open(make_path(filename), 'r') as file:
        out = file.read()
    return str(out)


def load_image(filename):
    with open(make_path(filename), 'rb') as file:
        out = file.read()
    return out


def test_version():
    assert page_loader.__version__ == '0.1.0'


@pytest.mark.parametrize("link,exs", [
    ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    ('https://pythonworld.ru/moduli/modul-os-path.html',
     'pythonworld-ru-moduli-modul-os-path.html'),
    ('http://pythonworld.ru/moduli/modul-os-path.html',
     'pythonworld-ru-moduli-modul-os-path.html'),
    ('tproger.ru/translations/regular-expression-python',
     'tproger-ru-translations-regular-expression-python.html'),
    ('tproger.ru/translations/regular-expression-python/', 'tproger-ru-translations-regular-expression-python.html')])
def test_get_name_for_page(link, exs):
    assert page_loader.page_loader.get_name(link) == exs


@pytest.mark.parametrize("link,exs,param1,param2", [
    ('https://pythonworld.ru/moduli/modul-os-path.html',
     'pythonworld-ru-moduli-modul-os-path_files', True, False),
    ('https://pythonworld.ru/moduli/modul-os-path.png',
     'pythonworld-ru-moduli-modul-os-path.png', False, True),
    ('pythonworld.ru/moduli/modul-os-path.jpg', 'pythonworld-ru-moduli-modul-os-path.jpg', False, True),
    ('pythonworld.ru/moduli/modul-os-path', 'pythonworld-ru-moduli-modul-os-path.html', False, True)])
def test_get_name_for(link, exs, param1, param2):
    assert page_loader.page_loader.get_name(
        link, is_folder=param1, is_files=param2) == exs
    assert page_loader.page_loader.get_name(
        link, is_folder=param1, is_files=param2) == exs


def test_cli_help_string():
    result = str(popen('poetry run page-loader -h').read())
    assert '-o OUTPUT, --output OUTPUT' in result
    assert 'positional arguments:\n  link' in result
    assert 'debug,info,warning,error,critical' in result


def test_cli_log_w_err(tmpdir):
    popen('poetry run page-loader -o {0} http://badsite'.format(tmpdir)).read()
    assert not listdir(tmpdir)


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


def test_update_links():
    input_page = read_out_exs('input_page.html')
    output_page = read_out_exs('output_page.html')
    assert page_loader.page_loader.update_links(input_page,
                                                'ru-hexlet-io-courses',
                                                'tmp/ru-hexlet-io-courses_files',
                                                'ru-hexlet-io-courses_files',
                                                '')[0] == output_page
