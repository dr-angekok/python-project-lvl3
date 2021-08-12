import pytest
from page_loader import __version__, page_loader


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.parametrize("url,exs", [
    ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    ('https://pythonworld.ru/moduli/modul-os-path.html', 'pythonworld-ru-moduli-modul-os-path.html'),
    ('http://pythonworld.ru/moduli/modul-os-path.html', 'pythonworld-ru-moduli-modul-os-path.html'),
    ('tproger.ru/translations/regular-expression-python', 'tproger-ru-translations-regular-expression-python.html'),
    ('tproger.ru/translations/regular-expression-python/', 'tproger-ru-translations-regular-expression-python.html')])

def test_get_name_for_page(url, exs):
    assert page_loader.get_name_for_page(url) == exs
