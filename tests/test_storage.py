from os import path

import pytest
from page_loader import errors
from page_loader.storage import make_folder, save_file, save_page


def make_path(file):
    PATH = 'tests/fixtures/'
    return '{0}{1}'.format(PATH, file)


def read_out_exs(filename):
    with open(make_path(filename), 'r') as file:
        out = file.read()
    return str(out)


def test_make_dir_error():
    PATH_TO_FOLDER = 'ru-wikipedia-org-wiki-Python'
    with pytest.raises(errors.MakeDirError):
        make_folder(PATH_TO_FOLDER)
        make_folder('//incorrect//dir')


def test_save_page_error(tmpdir):
    PAGE = read_out_exs('input_page.html')
    PATH_TO_PAGE = 'ru-wikipedia-org-wiki-Python.html'
    PATH = path.join(tmpdir, PATH_TO_PAGE)
    save_page(PATH, PAGE)
    with pytest.raises(errors.SavePageError):
        save_page(PATH, PAGE)
        save_page('//incorrect//file.path', PAGE)


def test_save_file_error(tmpdir):
    FILE = bytes(read_out_exs('input_page.html'), 'utf8')
    PATH_TO_PAGE = 'ru-wikipedia-org-wiki-Python.html'
    PATH = path.join(tmpdir, PATH_TO_PAGE)
    save_file(PATH, FILE)
    with pytest.raises(errors.SaveFileError):
        save_file(PATH, FILE)
        save_file('//incorrect//file.path', FILE)
