#!/usr/bin/env python3
"""Page dounload programm."""

import logging
from sys import exit

from page_loader import download
from page_loader.cli import get_arguments


def main():
    """Page dounload programm."""
    path_to_page, path_to_folder, log_level = get_arguments()
    try:
        page_filename = download(path_to_page, path_to_folder, log_level=log_level)
        print('Page saved at {0}'.format(page_filename))
    except Exception as e:
        logging.error('\nHas error: {0}'.format(e))
        exit(1)
    exit()


if __name__ == '__main__':
    main()
