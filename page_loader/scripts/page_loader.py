#!/usr/bin/env python3
"""Page dounload programm."""

import logging
from sys import exit

from page_loader import download
from page_loader.cli import parse_args


def main():
    """Page dounload programm."""
    path_to_page, path_to_folder, log_level = parse_args()
    try:
        page_filename = download(path_to_page, path_to_folder, log_level=log_level)
        print('Page saved at {0}'.format(page_filename))
    except Exception as e:
        logging.error('\nHas error: {0}'.format(e))
        exit(1)


if __name__ == '__main__':
    main()
