#!/usr/bin/env python3
"""Cli for the diff make."""
import argparse


def parse_args():
    """Pars command line parameters.

    Returns:
        tuple: str of first_file, second_file, format
    """
    parser = argparse.ArgumentParser(description='Generate diff of two files')
    parser.add_argument('path', metavar='<url>', type=str)
    arguments = parser.parse_args()
    return arguments.path
