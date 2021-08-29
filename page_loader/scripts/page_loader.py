#!/usr/bin/env python3
"""Page dounload programm."""

from sys import exit

from page_loader import download
from page_loader.cli import get_arguments


def main():
    """Page dounload programm."""
    path_to_page, path_to_folder, log_level = get_arguments()
    try:
        download(path_to_page, path_to_folder, log_level=log_level)
    except Exception as e:
        print('Has error {0}'.format(e))
    exit()


if __name__ == '__main__':
    main()
