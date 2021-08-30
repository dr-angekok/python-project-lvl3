"""Test module fore the page_loader."""
from os import path, popen

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
    ('https://site.com/blog/about/blog/about/assets/styles.css', 'site-com-blog-about-blog-about-assets-styles.css', False, True)])
def test_get_name_for(link, exs, param1, param2):
    assert page_loader.page_loader.get_name(
        link, is_folder=param1, is_files=param2) == exs
    assert page_loader.page_loader.get_name(
        link, is_folder=param1, is_files=param2) == exs


def test_cli_help_string():
    result = str(popen('poetry run page_loader -h').read())
    assert '-o OUTPUT, --output OUTPUT' in result
    assert 'positional arguments:\n  link' in result
    assert 'debug,info,warning,error,critical' in result


@pook.on
def test_download_page(tmpdir):
    PAGE_LINK_FOR_TEST = 'https://ru.wikipedia.org/wiki/Python'
    IMAGE_LINK_FOR_TEST = 'https://ru.wikipedia.org/wiki/assets/professions/nodejs.png'
    PATH_TO_FOLDER = tmpdir
    PATH_TO_PAGE = 'ru-wikipedia-org-wiki-Python.html'
    PAGE_RESPONSE = read_out_exs('input_page.html')

    page_mock = pook.get(PAGE_LINK_FOR_TEST, reply=200,
                         response_body=PAGE_RESPONSE)
    image_mock = pook.get(IMAGE_LINK_FOR_TEST, reply=200,
                          response_body=PAGE_RESPONSE)
    page_loader.download(PAGE_LINK_FOR_TEST, PATH_TO_FOLDER)
    assert page_mock.calls == 1
    assert path.isfile('{0}/{1}'.format(PATH_TO_FOLDER, PATH_TO_PAGE))
    assert image_mock.calls == 1


def test_update_links():
    input_page = read_out_exs('input_page.html')
    output_page = read_out_exs('output_page.html')
    assert page_loader.page_loader.update_links(input_page,
                                                'ru-hexlet-io-courses',
                                                'ru-hexlet-io-courses_files')[0].decode('utf-8') == output_page


def test_make_dir_error(tmpdir):
    PATH_TO_FOLDER = 'ru-wikipedia-org-wiki-Python'
    with pytest.raises(page_loader.page_loader.MakeDirError):
        page_loader.page_loader.make_folder(PATH_TO_FOLDER)
        page_loader.page_loader.make_folder('//incorrect//dir')


def test_save_page_error(tmpdir):
    PAGE = read_out_exs('input_page.html')
    PATH_TO_PAGE = 'ru-wikipedia-org-wiki-Python.html'
    PATH = path.join(tmpdir, PATH_TO_PAGE)
    page_loader.page_loader.save_page(PATH, bytes(PAGE, "utf8"))
    with pytest.raises(page_loader.page_loader.SavePageError):
        page_loader.page_loader.save_page(PATH, bytes(PAGE, "utf8"))
        page_loader.page_loader.save_page('//incorrect//file.path', bytes(PAGE, "utf8"))


@pook.on
@pytest.mark.parametrize("page_link,file_link,rep", [
    ('htts://pythonworld.ru/moduli/modul-os-path.html',
     'pythonworld-ru-moduli-modul-os-path_files', 404)])
def test_load_page_error(page_link, file_link, rep, tmpdir):
    PAGE_RESPONSE = read_out_exs('input_page.html')
    pook.get(page_link, reply=rep, response_body=PAGE_RESPONSE)
    inquiry = []
    inquiry.append([page_link, path.join(tmpdir, file_link)],)
    with pytest.raises(page_loader.page_loader.LoadFileError):
        page_loader.page_loader.save_files('htts://pythonworld.ru/', inquiry)
