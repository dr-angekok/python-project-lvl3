import pytest

from page_loader.url import to_filename, to_foldername, to_page_filename


@pytest.mark.parametrize("link,exs", [
    ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
    ('https://pythonworld.ru/moduli/modul-os-path.html', 'pythonworld-ru-moduli-modul-os-path.html'),
    ('http://pythonworld.ru/moduli/modul-os-path.html', 'pythonworld-ru-moduli-modul-os-path.html'),
    ('tproger.ru/translations/regular-expression-python', 'tproger-ru-translations-regular-expression-python.html'),
    ('tproger.ru/translations/regular-expression-python/', 'tproger-ru-translations-regular-expression-python.html'),
    ])
def test_get_name_for_page(link, exs):
    assert to_page_filename(link) == exs


@pytest.mark.parametrize("link,exs", [
    ('https://pythonworld.ru/moduli/modul-os-path.png', 'pythonworld-ru-moduli-modul-os-path.png'),
    ('pythonworld.ru/moduli/modul-os-path.jpg', 'pythonworld-ru-moduli-modul-os-path.jpg'),
    ('pythonworld.ru/moduli/modul-os-path', 'pythonworld-ru-moduli-modul-os-path.html'),
    ])
def test_get_name_for_file(link, exs):
    assert to_filename(link) == exs


def test_get_name_for_folder():
    assert to_foldername('https://pythonworld.ru/moduli/modul-os-path.html') == \
        'pythonworld-ru-moduli-modul-os-path_files'
