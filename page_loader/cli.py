#!/usr/bin/env python3
"""Cli for the diff make."""
import argparse


def get_arguments():
    """Pars command line parameters.

    Returns:
        tuple: str of first_file, second_file, format
    """
    parser = argparse.ArgumentParser(description='Generate diff of two files')
    parser.add_argument('link', type=str)
    parser.add_argument('-o', '--output',
                        type=str,
                        default='',
                        help='folder for saving link')
    arguments = parser.parse_args()
    return arguments.link, arguments.output