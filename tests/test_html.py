import page_loader


def make_path(file):
    PATH = 'tests/fixtures/'
    return '{0}{1}'.format(PATH, file)


def read_out_exs(filename):
    with open(make_path(filename), 'r') as file:
        out = file.read()
    return str(out)


def test_update_links():
    input_page = read_out_exs('input_page.html')
    output_page = read_out_exs('output_page.html')
    assert page_loader.html.prepare(input_page,
                                    'ru-hexlet-io-courses',
                                    'tmp/ru-hexlet-io-courses_files',
                                    'ru-hexlet-io-courses_files',
                                    '')[0] == output_page
