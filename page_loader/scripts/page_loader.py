#!/usr/bin/env python3
"""Page dounload programm."""

from page_loader import download
from page_loader.cli import parse_args


def main():
    """Page dounload programm."""
    path_to_page = parse_args()


if __name__ == '__main__':
    main()
