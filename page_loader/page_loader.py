"""Load url to files."""
from re import split, sub


def get_name_for_page(page_url):
    clear_path = sub(r'https://|http://|.html', '', page_url)
    file_path_list = split(r'[\/\.]', clear_path)
    clear_file_path_list = [world for world in file_path_list if world]
    file_path = '-'.join(clear_file_path_list)
    return '{0}.html'.format(file_path)


def download():
    print('is runed')


if __name__ == '__main__':
    print('is not a programm')
