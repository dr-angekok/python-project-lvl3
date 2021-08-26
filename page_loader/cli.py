#!/usr/bin/env python3
"""Cli for the diff make."""
import argparse


def get_arguments():
    """Pars command line parameters.

    Returns:
        tuple: str of link, output folder, logging level
    """
    parser = argparse.ArgumentParser(description='Load pages with files by url.')
    parser.add_argument('link',
                        type=str,
                        help='link for download page')
    parser.add_argument('-o', '--output',
                        type=str,
                        default='',
                        help='folder for saving link')
    parser.add_argument('-l', '--level',
                        type=str,
                        default='info',
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='logging level')
    arguments = parser.parse_args()
    return arguments.link, arguments.output, arguments.level