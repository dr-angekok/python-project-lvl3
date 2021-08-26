#!/usr/bin/env python3
"""Page dounload programm."""


from page_loader import download
from page_loader.cli import get_arguments


def main():
    """Page dounload programm."""
    path_to_page, path_to_folder, log_level = get_arguments()
    download(path_to_page, path_to_folder, log_level=log_level)


if __name__ == '__main__':
    main()
