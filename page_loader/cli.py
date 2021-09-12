"""Cli for the page loader."""
import argparse
import page_loader.logging


def parse_args():
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
                        help='folder for saving downloaded page')
    parser.add_argument('-l', '--level',
                        type=str,
                        default='info',
                        choices=page_loader.logging.LEVELS.keys(),
                        help='logging level')
    arguments = parser.parse_args()
    return arguments.link, arguments.output, arguments.level
